# -*- coding: utf-8 -*-

"""
Contiene una colección de funciones para obtener el valor de distintos
indicadores económicos de Chile.

## Funciones:

indicador_date : function
    Permite obtener el valor de un indicador económico dada una fecha.

indicador_year : function
    Permite obtener una serie de valores de un indicador dado un año.

## Atributos:

_indicadores : list
    Indicadores disponibles.

_date : str
    Fecha de "hoy" en formato "dd-mm-yyyy".

_year : str
    Año presente en formato "yyyy".
"""

__author__ = "Matías Schiaffino Tyrer"
__contact__ = "matias.scht@gmail.com"
__date__ = "2021/03/11"
__deprecated__ = False
__email__ =  "matias.scht@gmail.com"
__license__ = "GPLv3"
__maintainer__ = "Matías Schiaffino Tyrer"
__status__ = "Desarrollo"
__version__ = "1.0.0"

#
#
#

import json
import requests
from datetime import datetime
from pandas import DataFrame, Timestamp, to_datetime

# Lista de indicadores disponibles
_indicadores = ["uf", "ivp", "dolar", "dolar_intercambio", "euro", "ipc",
                "utm", "imacec", "tpm", "libra_cobre", "tasa_desempleo",
                "bitcoin"]

# Fecha de "ahora"
_date = datetime.now().strftime("%d-%m-%Y")

# Año presente
_year = datetime.now().strftime("%Y")

#
#
#

def indicador_date(indicador: str="uf", date: str=_date) -> float:
    
    """
    ## Descripción:
    
    Recibe un tipo de indicador y fecha y devuelve el valor de dicho indicador
    económico para la fecha ingresada.

    ## Parámetros:

    indicador : str
        Tipo de indicador económico que se quiere consultar.

    date : str, opcional
        Fecha para la que se quiere conocer el indicador. Debe estar
        en formato "dd-mm-yyyy". Por defecto es la fecha de "hoy".

    ## Retorno:

    float
        Valor del indicador para la fecha ingresada.
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

#
#
#

def indicador_year(indicador: str="uf", year: str=_year, date_index: bool=False) -> DataFrame:
    
    """
    ## Descripción:
    
    Recibe un tipo de indicador y año y devuelve la serie completa de
    valores para el indicador de todo el año.

    ## Parámetros:

    indicador : str
        Tipo de indicador económico que se quiere consultar.

    year : str, opcional. Por defecto el año presente
        Año para la que se quiere conocer el indicador. Debe estar
        en formato "yyyy".

    date_index : bool, opcional. Por defecto False.
        Si es True, el campo de fecha pasa a ser el index del
        DataFrame.

    ## Retorno:

    pandas.DataFrame
        Serie de valores de todo el año del indicador.
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