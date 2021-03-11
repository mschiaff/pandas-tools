# -*- coding: utf-8 -*-

"""
Contiene una colección de funciones para realizar operaciones
sobre RUT.

## Funciones:

calc_dv : function
    Calcula el dígito de un único correlativo de RUT.

get_dv : function
    Calcula el dígito verificador de una serie de correlativos
    de RUT contenidos en un pandas.DataFrame.
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

from re import sub
from typing import Union
from itertools import cycle
from pandas import DataFrame

#
#
#

def calc_dv(rut: Union[int, str]) -> Union[int, str]:

    """
    ## Descripción:

    Calcula el dígito verificador de un correlativo de RUT.

    ## Parámetros:

    rut: int, str
        Correlativo de RUT.

    ## Retorno:

    int, str
        Dígito verificador del correlativo de RUT.
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
    
    # Si el dv es 11, entonces se reemplaza por cero (0)
    elif dv == 11:
        dv = 0
    
    # Si el dv es distinto de 10 u 11, entonces se conserva como está
    else:
        pass

    # Devuelve el dígito verificador como entero o string dependiendo
    # del caso
    return dv

#
#
#

def get_dv(df: DataFrame, rut_fname: str, dv_fname: str="DV",
            rut_dv: bool=False, rut_dv_fname: str="RUT_DV",
            zero_filled: bool=False, with_dot: bool=False) -> DataFrame:
    
    """
    ## Descripción:

    Calcula el dígito verificador de correlativos de RUT contenidos en un
    pandas.DataFrame.

    ## Parámetros:

    df : pandas.DataFrame
        Contiene los correlativos de RUT.
    
    rut_field_name : str
        Nombre del campo que contiene los correlativos de RUT.
    
    dv_field : str, opcional. Por defecto "DV"
        Nombre que se quiere para el campo de salida que contendrá los dígitos 
        verificadores de cada correlativo de RUT.

    rut_dv : bool, opcional. Por defecto False
        Si es True, crea un campo adicional que concatena el correlativo del
        RUT con el dígito verificador calculado.

    rut_dv_fname : str, opcional. Por defecto "RUT_DV"
        Nombre que tendrá el campo adicional cuando rut_dv es True.

    zero_filled : bool, opcional. Por defecto False
        Aplica cuando rut_dv es True. Agrega ceros al principio del correlativo
        hasta completar 8 caracteres, luego concatena con "DV".

    with_dot : bool, opcional. Por defecto False
        Aplica cuando rut_dv es True. Agrega puntos como separador de miles al
        correlativo del RUT, luego concatena con DV. También se puede usar cuadno
        zero_filles es True.

    ## Consideraciones:

    - Cuando rut_dv es True, independiente del valor que tengan los parámetros
    zero_filles y with_dot, el nombre del nuevo campo siempre será rut_dv_fname.

    ## Retorno:

    pandas.DataFrame
    """

    # Aplica la función _calc_dv al df
    df[dv_fname] = df[rut_fname].apply(calc_dv)

    # Si rut_dv es True
    if rut_dv:

        df[rut_dv_fname] = df[rut_fname]

        # Si zero_filles es True
        if zero_filled:

            # Agrega ceros al principio del correlativo hasta completar 8 caracteres
            df[rut_dv_fname] = df[rut_dv_fname].apply(lambda row: str(row).zfill(8))

        # Si with_dot es True
        if with_dot:

            # Aplica punto como separador de miles al correlativo de RUT
            df[rut_dv_fname] = df[rut_dv_fname].apply(lambda row: sub("(\d)(?=(\d{3})+(?!\d))", r"\1.", str(row)))

        # Crea un campo de nombre rut_dv_fname que concatena el correlativo
        # de rut con el dv calculado separado por guión ("-")
        df[rut_dv_fname] = df[rut_dv_fname].map(str) + "-" + df[dv_fname].map(str)
    
    # Si rut_dv es False
    else:

        # No hace nada
        pass

    # Devuelve el DataFrame
    return df