# -*- coding: utf-8 -*-

from typing import Union
from itertools import cycle
from pandas import DataFrame

def _calc_dv(rut: Union[int, str]) -> Union[int, str]:

    """
    ## Descripción:

    Función auxiliar que realiza el cálculo del dígito verificador del
    correlativo de RUT. También se puede usar para cálculos individuales.

    ## Parámetros:

    - rut: int o str con el correlativo de RUT.

    ## Retorno:

    Dígito verificador del correlativo de RUT pasado como parámetro como
    entero o string, dependiendo del resultado del dígito verificador.
    """

    # El correlativo de RUT recibido se pasa a una lista de enteros
    rut = [int(n) for n in str(rut)]

    # Crea lista iterable en ciclo dentro del intervalo [2, 7]
    factors = cycle([x for x in range(2,8)])

    # Inicializa en cero la variable con la suma acumulada del producto
    # entre los dígitos del correlativo de RUT y la lista de factores
    sum = 0

    # Multiplica cada dígito del correlativo de RUT por cada elemento de
    # la lista de factores
    for digit, factor in zip(reversed(rut), factors):

        # Cada producto se acumula en "sum"
        sum += digit * factor

    # El dígito verificador del RUT ("dv") es la diferencia entre 11 y el
    # resto del cociente entre la suma acumulada y 11 (módulo)
    dv = 11 - (sum % 11)

    # En Chile, si el dv es 10, entonces se reemplaza por "K"
    if dv == 10:
        dv = "K"
    
    # Si el dv es distinto de 10, entonces se conserva como está
    else:
        pass

    # Devuelve el dígito verificador como entero o string dependiendo
    # del caso
    return dv

def get_dv(df: DataFrame, rut_field_name: str, dv_field: str="DV") -> DataFrame:
    """
    ## Descripción:

    Recibe un pandas.DataFrame con un campo que contenga sólo correlativos de
    RUT y calcula del dígito verificador.

    ## Parámetros:

    - df: DataFrame que contiene el campo con correlativos de RUT.
    
    - rut_field_name: String con el nombre del campo que contiene
    los correlativos de RUT en df.
    
    - dv_field: Opcional. El nombre que se quiere para el campo de
    salida que contendrá los dígitos verificadores de cada correlativo
    de RUT. Por defecto es "DV".

    ## Retorno:

    Devuelve el mismo DataFrame pasado como parámetro.
    """

    # Aplica la función _calc_dv al df
    df[dv_field] = df[rut_field_name].apply(_calc_dv)

    # Devuelve el mismo DataFrame
    return df