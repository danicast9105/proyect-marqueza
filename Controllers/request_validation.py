def obtener_campos_faltantes(data, campos_requeridos):
    return [
        campo
        for campo in campos_requeridos
        if campo not in data
        or data[campo] is None
        or (isinstance(data[campo], str) and not data[campo].strip())
    ]
