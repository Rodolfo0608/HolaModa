import pytest

from app import create_app


def test_summary_matches_known_values(client):
    response = client.get('/api/summary')
    assert response.status_code == 200
    assert response.json == {'records':3,'customers':3,'total_amount_usd':60.6,
                             'average_amount_usd':20.2,'average_rating':4.5,'discounted_records':2}


def test_filters_combine_and_totals_reconcile(client):
    query = '?category=Clothing&season=Winter&gender=Female&discounted=1'
    summary = client.get('/api/summary'+query).json
    groups = client.get('/api/groups/category'+query).json['data']
    detail = client.get('/api/purchases'+query).json
    assert summary['records'] == detail['total'] == sum(r['records'] for r in groups) == 1
    assert summary['total_amount_usd'] == sum(r['amount_usd'] for r in groups) == 10.1


def test_empty_selection_returns_no_fake_averages(client):
    result = client.get('/api/summary?category=NotPresent').json
    assert result['records'] == result['total_amount_usd'] == 0
    assert result['average_amount_usd'] is None
    assert client.get('/api/groups/item?category=NotPresent').json['data'] == []


def test_pagination_is_stable(client):
    first = client.get('/api/purchases?per_page=2').json
    second = client.get('/api/purchases?per_page=2&page=2').json
    assert first['total'] == 3 and first['pages'] == 2
    assert [r['customer_id'] for r in first['data']] == [1,2]
    assert [r['customer_id'] for r in second['data']] == [3]
    assert client.get('/api/purchases?page=10').json['data'] == []


@pytest.mark.parametrize('url', [
    '/api/purchases?page=0','/api/purchases?page=abc','/api/purchases?per_page=101',
    '/api/purchases?per_page=-1','/api/summary?discounted=2','/api/summary?unknown=x',
    '/api/summary?category=a&category=b','/api/groups/not_a_column',
    '/api/purchases?page=1&page=2',
])
def test_invalid_requests_have_explicit_errors(client, url):
    response = client.get(url)
    assert response.status_code == 400
    assert response.json['error']['code'] == 'invalid_request'


def test_sql_injection_stays_a_filter_value(client):
    response = client.get('/api/summary', query_string={'category': "Clothing' OR 1=1 --"})
    assert response.status_code == 200 and response.json['records'] == 0
    assert client.get('/api/health').json['rows'] == 3


def test_missing_database_is_503_without_creating_file(tmp_path):
    missing = tmp_path / 'missing.db'
    client = create_app({'TESTING':True,'DATABASE':str(missing)}).test_client()
    response = client.get('/api/health')
    assert response.status_code == 503
    assert response.json['error']['code'] == 'data_unavailable'
    assert not missing.exists()


def test_contract_pipeline_and_static_pages(client):
    assert client.get('/api/pipeline').json['latest_run']['row_count'] == 3
    assert client.get('/api/filters').json['category'] == ['Clothing','Footwear']
    contract = client.get('/api/openapi.json').json
    assert contract['openapi'] == '3.0.3'
    assert '/api/summary' in contract['paths']
    for path in ['/', '/docs', '/static/app.js', '/static/vendor/chart.umd.js', '/static/vendor/swagger-ui-bundle.js']:
        response = client.get(path)
        assert response.status_code == 200
        assert response.headers['X-Content-Type-Options'] == 'nosniff'
    assert client.post('/api/purchases').status_code == 405
    assert client.get('/missing').status_code == 404
