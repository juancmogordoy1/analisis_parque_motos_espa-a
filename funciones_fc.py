
# FUNCIONES AUXILIARES – PROYECTO MOTOS ESPAÑA
# Archivo: funciones_fc.py

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re


# ------------------------------------------------------------
# LIMPIEZA NUMÉRICA
# ------------------------------------------------------------

def limpiar_numerico(serie):
    return (
        serie.astype(str)
        .str.replace('.', '', regex=False)   # elimina separadores de miles
        .str.replace(',', '.', regex=False)  # normaliza coma decimal
        .astype(float)                       # convierte a float
    )
# Limpia columnas numéricas “simples”
# Útil cuando los datos vienen relativamente limpios


def limpiar_numerico_robusto(serie):
    return (
        serie.astype(str)
        .str.replace('\u00a0', ' ', regex=False)       # reemplaza espacios raros (NBSP)
        .str.strip()                                   # quita espacios inicio/fin
        .str.replace('.', '', regex=False)             # elimina separador de miles
        .str.replace(',', '.', regex=False)            # convierte coma decimal a punto
        .str.extract(r'([-+]?\d*\.?\d+)')[0]           # extrae número aunque venga con texto
        .astype(float)                                 # convierte a float
    )
# Limpia numéricos “sucios”:


# ------------------------------------------------------------
# UTILIDADES DE DATAFRAME
# ------------------------------------------------------------

def buscar_columna(df, palabras_clave):
    for col in df.columns:
        for palabra in palabras_clave:
            if palabra.upper() in col.upper():
                return col
    raise ValueError(f"No se encontró columna con: {palabras_clave}")
# Busca una columna aunque el nombre cambie entre datasets
# usando palabras clave parciales 


# ------------------------------------------------------------
# CLASIFICACIÓN DE ANTIGÜEDAD – DISTINTIVO AMBIENTAL
# ------------------------------------------------------------

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
# Clasifica antigüedad cuando el distintivo viene en formato largo/textual
# Ej: "Etiqueta B", "Etiqueta C", "ECO", "Cero emisiones"


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
# Versión “limpia” para distintivos inconsistentes o abreviados
# Ej: "B", "C", "E", "0", "--", vacío (muy común en Madrid / BCN)


# ------------------------------------------------------------
# WEB SCRAPING
# ------------------------------------------------------------

def realizar_scraping(url, parser='html.parser'):
    """
    Realiza scraping básico de una URL y devuelve un objeto BeautifulSoup
    """
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, parser)
# Función genérica de scraping
# Separa la lógica web del notebook y permite reutilización


