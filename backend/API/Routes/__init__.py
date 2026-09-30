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
from .auth_bp import auth_bp
from .detalle_cotizacion_bp import detalle_cotizacion_bp
from .recuperacion_contrasena_bp import recuperacion_contrasena_bp
from .bitacora_auditoria_bp import bitacora_auditoria_bp


PREFIX = '/api'


def load_routes(app):
    app.url_map.strict_slashes = False
    app.register_blueprint(cliente_bp, url_prefix=f'{PREFIX}/clientes')
    app.register_blueprint(contacto_bp, url_prefix=f'{PREFIX}/contactos')
    app.register_blueprint(cotizaciones_bp, url_prefix=f'{PREFIX}/cotizaciones')
    app.register_blueprint(detalles_etc_bp, url_prefix=f'{PREFIX}/detalles-etc')
    app.register_blueprint(etc_bp, url_prefix=f'{PREFIX}/etc')
    app.register_blueprint(insumos_bp, url_prefix=f'{PREFIX}/insumos')
    app.register_blueprint(persona_bp, url_prefix=f'{PREFIX}/personas')
    app.register_blueprint(produ_insum_bp, url_prefix=f'{PREFIX}/productos-insumos')
    app.register_blueprint(productos_bp, url_prefix=f'{PREFIX}/productos')
    app.register_blueprint(proveedor_bp, url_prefix=f'{PREFIX}/proveedores')
    app.register_blueprint(usuarios_bp, url_prefix=f'{PREFIX}/usuarios')
    app.register_blueprint(vent_prod_bp, url_prefix=f'{PREFIX}/ventas-productos')
    app.register_blueprint(ventas_bp, url_prefix=f'{PREFIX}/ventas')
    app.register_blueprint(documentacion_bp, url_prefix=f'{PREFIX}/documentacion')
    app.register_blueprint(auth_bp, url_prefix=f'{PREFIX}/auth')
    app.register_blueprint(detalle_cotizacion_bp, url_prefix=f'{PREFIX}/detalle-cotizacion')
    app.register_blueprint(recuperacion_contrasena_bp, url_prefix=f'{PREFIX}/recuperacion-contrasena')
    app.register_blueprint(bitacora_auditoria_bp, url_prefix=f'{PREFIX}/bitacora-auditoria')
