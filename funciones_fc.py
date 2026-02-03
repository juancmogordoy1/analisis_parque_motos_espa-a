import pandas as pd
import requests
from bs4 import BeautifulSoup
import re


def buscar_columna(df, palabras_clave):
    for col in df.columns:
        for palabra in palabras_clave:
            if palabra.upper() in col.upper():
                return col
    raise ValueError(f"No se encontró columna con: {palabras_clave}")
# Es para encontrar una columna aunque su nombre cambie entre datasets
# usando palabras clave parciales (mayúsculas, minúsculas o variantes)


def clasificar_antiguedad(etiqueta):
    e = str(etiqueta).lower()
    if any(x in e for x in ['sin', 'sense', 'no consta', 'nan']):
        return 'Critico (+20 anos)'
    if 'etiqueta b' in e:
        return 'Envejecido (15-20 anos)'
    if 'etiqueta c' in e:
        return 'Moderno (10-15 anos)'
    if any(x in e for x in ['0', 'eco', 'cero']):
        return 'Nuevo-Eco (<10 anos)'
    return 'Otros'
# Es para clasificar la antigüedad aproximada del vehículo
# cuando el distintivo ambiental viene en formato textual
# como "Etiqueta B", "Etiqueta C", "ECO" o "Cero emisiones"


def clasificar_antiguedad_limpia(etiqueta):
    e = str(etiqueta).strip().lower()

    if e in ["", "nan", "none", "--"] or "sin" in e or "sense" in e or "no consta" in e:
        return "Critico (+20 anos)"

    if e == "b" or "etiqueta b" in e:
        return "Envejecido (15-20 anos)"

    if e == "c" or "etiqueta c" in e:
        return "Moderno (10-15 anos)"

    if e in ["e", "eco"] or "eco" in e:
        return "Nuevo-Eco (<10 anos)"

    if e in ["0", "zero", "cero"] or re.search(r"\b0\b", e) or "cero" in e or "zero" in e:
        return "Nuevo-Eco (<10 anos)"

    return "Otros"
# Es para clasificar la antigüedad cuando los distintivos
# vienen en formato corto o inconsistente (Madrid / BCN):
# "B", "C", "E", "0", "--", vacíos, etc.


def limpiar_numerico(serie):
    return (
        serie.astype(str)
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False)
        .astype(float)
    )
# Es para limpiar columnas numéricas sim
