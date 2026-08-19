from .user_bp import us_bp
from .car_bp import car_bp

from .usuarios_bp import usuario_bp
from .clientes_bp import cliente_bp
from .productos_bp import producto_bp
from .insumos_bp import insumo_bp
from .cotizaciones_bp import cotizacion_bp
from .ventas_bp import venta_bp
from .proveedores_bp import proveedor_bp


def load_routes(app):
    # rutas de ejemplo (no forman parte del modelo real del proyecto)
    app.register_blueprint(us_bp, url_prefix='/users')
    app.register_blueprint(car_bp, url_prefix='/cars')

    # rutas del proyecto Marqueza.C
    app.register_blueprint(usuarios_bp,    url_prefix='/usuarios')
    app.register_blueprint(clientes_bp,    url_prefix='/clientes')
    app.register_blueprint(productos_bp,   url_prefix='/productos')
    app.register_blueprint(insumos_bp,     url_prefix='/insumos')
    app.register_blueprint(cotizaciones_bp, url_prefix='/cotizaciones')
    app.register_blueprint(ventas_bp,      url_prefix='/ventas')
    app.register_blueprint(proveedores_bp,  url_prefix='/proveedores')


# http://127.0.0.1:5000/usuarios/          GET
# http://127.0.0.1:5000/usuarios/create    POST
# http://127.0.0.1:5000/usuarios/edit/<id> PUT
# http://127.0.0.1:5000/usuarios/delete/<id> DELETE

# http://127.0.0.1:5000/clientes/          GET
# http://127.0.0.1:5000/clientes/create    POST
# http://127.0.0.1:5000/clientes/edit/<id> PUT
# http://127.0.0.1:5000/clientes/delete/<id> DELETE

# http://127.0.0.1:5000/productos/          GET
# http://127.0.0.1:5000/productos/create    POST
# http://127.0.0.1:5000/productos/edit/<id> PUT
# http://127.0.0.1:5000/productos/delete/<id> DELETE

# http://127.0.0.1:5000/insumos/          GET
# http://127.0.0.1:5000/insumos/create    POST
# http://127.0.0.1:5000/insumos/edit/<id> PUT
# http://127.0.0.1:5000/insumos/delete/<id> DELETE

# http://127.0.0.1:5000/cotizaciones/          GET
# http://127.0.0.1:5000/cotizaciones/create    POST
# http://127.0.0.1:5000/cotizaciones/edit/<id> PUT
# http://127.0.0.1:5000/cotizaciones/delete/<id> DELETE

# http://127.0.0.1:5000/ventas/          GET
# http://127.0.0.1:5000/ventas/create    POST
# http://127.0.0.1:5000/ventas/edit/<id> PUT
# http://127.0.0.1:5000/ventas/delete/<id> DELETE

# http://127.0.0.1:5000/proveedores/          GET
# http://127.0.0.1:5000/proveedores/create    POST
# http://127.0.0.1:5000/proveedores/edit/<id> PUT
# http://127.0.0.1:5000/proveedores/delete/<id> DELETE
