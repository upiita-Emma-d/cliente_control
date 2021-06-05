from datos_csv import retorno_de_json
from envio_de_datos import envio_post

def funcion_de_labview(direccion):
    datos = retorno_de_json(direccion)
    respuesta = envio_post(datos)
    return respuesta
