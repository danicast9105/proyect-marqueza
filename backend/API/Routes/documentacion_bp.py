from flask import Blueprint, render_template_string, send_from_directory

documentacion_bp = Blueprint('documentacion', __name__)

@documentacion_bp.route('/swagger.json')
def swagger_json():
    return send_from_directory('.', 'swagger.json')

@documentacion_bp.route("/")
def swagger_ui():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
      <title>CCCCC</title>
      <link href="/static/swagger-ui/swagger-ui.css" rel="stylesheet" />
    </head>
    <body>
      <div id="swagger-ui"></div>
      <script src="/static/swagger-ui/swagger-ui-bundle.js"></script>
      <script>
        const ui = SwaggerUIBundle({
          url: "./swagger.json",
          dom_id: '#swagger-ui',
        });
      </script>
    </body>
    </html>
    """)
 