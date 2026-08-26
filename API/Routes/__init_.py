from .cliente_bp import cliente_bp
from .contacto_bp import contacto_bp
from .cotizaciones_bp import cotizaciones_bp
from .detalles_etc_bp import detalles_etc_bp
from .etc_bp import etc_bp
from .insumos_bp import insumos_bp
from .persona_bp import persona_bp
from .produ_insum_bp import produ_insum_bp
from .productos_bp import productos_bp
from .proveedor_bp import proveedor_bp
from .usuarios_bp import usuarios_bp
from .vent_prod_bp import vent_prod_bp
from .ventas_bp import ventas_bp
from .documentacion_bp import documentacion_bp


def load_routes(app):
    app.register_blueprint(cliente_bp, url_prefix='/clientes')
    app.register_blueprint(contacto_bp, url_prefix='/contactos')
    app.register_blueprint(cotizaciones_bp, url_prefix='/cotizaciones')
    app.register_blueprint(detalles_etc_bp, url_prefix='/detalles-etc')
    app.register_blueprint(etc_bp, url_prefix='/etc')
    app.register_blueprint(insumos_bp, url_prefix='/insumos')
    app.register_blueprint(persona_bp, url_prefix='/personas')
    app.register_blueprint(produ_insum_bp, url_prefix='/productos-insumos')
    app.register_blueprint(productos_bp, url_prefix='/productos')
    app.register_blueprint(proveedor_bp, url_prefix='/proveedores')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    app.register_blueprint(vent_prod_bp, url_prefix='/ventas-productos')
    app.register_blueprint(ventas_bp, url_prefix='/ventas')
    app.register_blueprint(documentacion_bp, url_prefix='/documentacion')