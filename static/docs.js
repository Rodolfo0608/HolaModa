window.addEventListener('DOMContentLoaded', () => {
  SwaggerUIBundle({url: '/api/openapi.json', dom_id: '#swagger-ui', deepLinking: true,
    supportedSubmitMethods: ['get'], validatorUrl: null});
});
