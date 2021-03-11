# -*- coding: utf-8 -*-

import json
import requests
from datetime import datetime
from pandas import DataFrame, Timestamp, to_datetime

# Fecha de "ahora"
_date = datetime.now().strftime("%d-%m-%Y")

# Año de "ahora"
_year = datetime.now().strftime("%Y")


def indicador_date(indicador: str="uf", date: str=_date) -> float:
    
    """
    ## Descripción:
    
    Recibe un tipo de indicador y fecha y devuelve el valor de dicho indicador
    económico para la fecha ingresada.

    ## Parámetros:

    - indicador: string con el tipo de indicador económico que se quiere consultar.

    - date: string con la fecha para la que se quiere conocer el indicador. Debe estar
    en formato "dd-mm-yyyy". Por defecto es la fecha de "hoy".

    ## Retorno:

    Float con el valor del indicador para la fecha ingresada.
    """
    
    # URL de la API donde se consultan los indicadores
    url = f"https://mindicador.cl/api/{indicador}/{date}"

    # Recibe los resultados de la consulta
    response = requests.get(url)

    # Los resultados se vuelcan en json
    data = json.loads(response.text.encode("utf-8"))

    # Intenta extraer el valor del indicador
    try:
        value = data["serie"][0]["valor"]
    
    # Si el valor no existe, entonces levanta un error
    except IndexError:
        raise IndexError("Valor no disponible para fecha ingresada.") from None

    # Si el indicador no existe, entonces levanta un error
    except KeyError:
        raise KeyError("Indicador no existe o no está disponible.") from None

    # Si no ocurre una excepción, retorna el indicador
    return value


def indicador_year(indicador: str="uf", year: str=_year, date_index: bool=False) -> DataFrame:
    
    """
    ## Descripción:
    
    Recibe un tipo de indicador y año y devuelve la serie completa de
    valores para el indicador de todo el año.

    ## Parámetros:

    - indicador: string con el tipo de indicador económico que se quiere consultar.

    - year: string con el año para la que se quiere conocer el indicador. Debe estar
    en formato "yyyy". Por defecto es el presente año.

    - date_index: Por defecto es False. Si es True, el campo de fecha pasa a ser el
    index del DataFrame.

    ## Retorno:

    pandas DataFrame con la serie de valores de todo el año del indicador.
    """
    
    # URL de la API donde se consultan los indicadores
    url = f"https://mindicador.cl/api/{indicador}/{year}"

    # Recibe los resultados de la consulta
    response = requests.get(url)

    # Los resultados se vuelcan en json
    data = json.loads(response.text.encode("utf-8"))
    
    # Pasa la serie a DataFrame
    data = DataFrame.from_dict(data["serie"])

    # Convierte de string a datetime el campo de fecha
    data["fecha"] = data["fecha"].apply(to_datetime)

    # Convierte campo de fecha a datetime.date
    data["fecha"] = data["fecha"].apply(Timestamp.date)

    # Si date_index es True, convierte el campo de fecha en el index
    if date_index:
        data.set_index("fecha", inplace=True)
    
    # En caso contrario, la fecha y los valores son campos del DataFrame
    else:
        pass

    return data