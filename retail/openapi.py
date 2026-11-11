"""Contrato de consultas de la muestra de compras."""


def specification():
    def obj(properties):
        return {'type': 'object', 'properties': properties, 'required': list(properties)}
    integer = {'type': 'integer'}
    string = {'type': 'string'}
    numeric = {'type': 'number'}
    nullable = {'type': 'number', 'nullable': True}
    summary = obj(dict(records=integer, customers=integer, total_amount_usd=numeric,
                       average_amount_usd=nullable, average_rating=nullable, discounted_records=integer))
    group = obj(dict(label=string, records=integer, amount_usd=numeric))
    purchase = obj(dict(customer_id=integer, age=integer, gender=string, item=string, category=string,
                        amount_usd=numeric, season=string, discounted=integer, rating=numeric))
    run = obj(dict(id=integer, loaded_at={'type':'string','format':'date-time'}, source_name=string,
                   sha256=string, row_count=integer, duration_ms=integer))
    filters = [{'name': name, 'in': 'query', 'required': False, 'schema': {'type':'string', 'maxLength':120},
                'description': 'Valor exacto de /api/filters. Omitir para incluir todos.'}
               for name in ('category','season','gender')]
    filters.append({'name':'discounted','in':'query','schema':{'type':'string','enum':['0','1']},
                    'description':'0: sin descuento; 1: con descuento. Omitir para incluir todos.'})
    error = obj({'error': obj({'code':string,'message':string})})

    def operation(title, schema, parameters=None, example=None):
        content = {'schema': schema}
        if example is not None:
            content['example'] = example
        return {'get': {'summary':title,'parameters':parameters or [], 'responses':{
            '200':{'description':'Consulta completada','content':{'application/json':content}},
            '400':{'description':'Parámetro inválido','content':{'application/json':{'schema':error}}},
            '503':{'description':'Datos sin cargar o base no disponible','content':{'application/json':{'schema':error}}},
        }}}
    return {
        'openapi':'3.0.3',
        'info':{'title':'HolaModa · API de tendencias de compra','version':'1.0.0',
                'description':'Muestra sintética de Kaggle. Una observación por cliente. Los importes están en USD. API local de consulta, sin operaciones de escritura. Filtros combinables con AND.'},
        'servers':[{'url':'/'}],
        'paths':{
            '/api/health':operation('Disponibilidad de la base',obj({'status':string,'rows':integer})),
            '/api/filters':operation('Valores disponibles para filtros',obj({n:{'type':'array','items':string} for n in ('category','season','gender')})),
            '/api/summary':operation('Indicadores de la selección',summary,filters),
            '/api/groups/{dimension}':operation('Totales agrupados en orden descendente por monto',obj({'dimension':string,'data':{'type':'array','items':group}}),
                [{'name':'dimension','in':'path','required':True,'schema':{'type':'string','enum':['category','season','item','payment']}}]+filters),
            '/api/purchases':operation('Detalle paginado ordenado por cliente',obj({'data':{'type':'array','items':purchase},'page':integer,'per_page':integer,'total':integer,'pages':integer}),
                filters+[{'name':'page','in':'query','schema':{'type':'integer','minimum':1,'maximum':1000000,'default':1}},
                         {'name':'per_page','in':'query','schema':{'type':'integer','minimum':1,'maximum':100,'default':10}}]),
            '/api/pipeline':operation('Última carga confirmada y huella de la fuente',obj({'latest_run':{**run,'nullable':True}})),
        }
    }
