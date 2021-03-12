# pandas-tools
Colección de módulos con funciones de Python 3 que me han resultado útiles o interesantes a la hora de procesar, calcular y resumir datos contenidos en DataFrames y Series de la librería pandas.

Los módulos contenidos en el repositorio están diseñados para ser independientes unos de otros, a menos que se indique lo contrario, y son de propósito general. Aunque con la contribución suficiente no se descarta transformar esto en un package colaborativo.

# Módulos

## Rut.py
Contiene funciones para realizar operaciones sobre correlativos de RUT, como calcular el dígito para un único RUT o para una serie de estos contenidos en un pandas.DataFrame con diferentes formatos de salida.

## Indicadores.py
Contiene funciones para consultar en una API los principales indicadores económicos de Chile, como la UF, dólar, tasa de desempleo, etc., ya sea por fecha o una serie de valores para un año completo.

La API proviene de la página www.mindicador.cl (Cristhopher Riquelme), la que es totalmente gratuita y se sostiene en base a donaciones, por lo que también quedan invitados a entregar su aporte para que la API siga funcionando.
