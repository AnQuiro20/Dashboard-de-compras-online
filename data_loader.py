"""
Módulo para carga y procesamiento de datos
"""
import pandas as pd
import json
import streamlit as st

@st.cache_data
def cargar_datos(archivo='compras.json'):
    """
    Carga datos desde un archivo JSON o CSV
    """
    try:
        if archivo.endswith('.json'):
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            df = pd.DataFrame(datos)
        else:
            df = pd.read_csv(archivo)
        
        # Procesamiento de datos
        df = procesar_datos(df)
        return df
        
    except FileNotFoundError:
        st.error(f"Archivo {archivo} no encontrado.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)}")
        return pd.DataFrame()

def procesar_datos(df):
    """
    Realiza transformaciones comunes en los datos
    """
    # Convertir fecha
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    # Calcular total de compra
    df['total_compra'] = df['cantidad'] * df['precio']
    
    # Extraer componentes de fecha
    df['mes'] = df['fecha'].dt.strftime('%Y-%m')
    df['mes_nombre'] = df['fecha'].dt.strftime('%B %Y')
    df['año'] = df['fecha'].dt.year
    df['trimestre'] = df['fecha'].dt.quarter
    df['semana'] = df['fecha'].dt.isocalendar().week
    df['dia_semana'] = df['fecha'].dt.day_name()
    
    # Ordenar por fecha
    df = df.sort_values('fecha')
    
    return df

def aplicar_filtros(df, plataforma_seleccionada, categoria_seleccionada, rango_fechas):
    """
    Aplica filtros al DataFrame
    """
    df_filtrado = df.copy()
    
    # Filtrar por rango de fechas
    if len(rango_fechas) == 2:
        df_filtrado = df_filtrado[
            (df_filtrado['fecha'].dt.date >= rango_fechas[0]) & 
            (df_filtrado['fecha'].dt.date <= rango_fechas[1])
        ]
    
    # Filtrar por plataforma
    if plataforma_seleccionada != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['plataforma'] == plataforma_seleccionada]
    
    # Filtrar por categoría
    if categoria_seleccionada != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['categoria'] == categoria_seleccionada]
    
    return df_filtrado

def obtener_opciones_filtros(df):
    """
    Obtiene opciones únicas para los filtros
    """
    plataformas = ['Todas'] + sorted(df['plataforma'].unique().tolist())
    categorias = ['Todas'] + sorted(df['categoria'].unique().tolist())
    
    return plataformas, categorias

def cargar_datos_subidos(archivo_subido):
    """
    Carga datos desde un archivo subido
    """
    try:
        if archivo_subido.name.endswith('.json'):
            datos = json.load(archivo_subido)
            df = pd.DataFrame(datos)
        else:
            df = pd.read_csv(archivo_subido)
        
        df = procesar_datos(df)
        return df
        
    except Exception as e:
        st.error(f"Error al cargar archivo: {str(e)}")
        return pd.DataFrame()

def obtener_resumen_estadistico(df):
    """
    Obtiene un resumen estadístico de los datos
    """
    if df.empty:
        return {}
    
    resumen = {
        'total_compras': len(df),
        'monto_total': df['total_compra'].sum(),
        'gasto_promedio': df['total_compra'].mean(),
        'gasto_maximo': df['total_compra'].max(),
        'gasto_minimo': df['total_compra'].min(),
        'primera_compra': df['fecha'].min(),
        'ultima_compra': df['fecha'].max(),
        'plataformas_unicas': df['plataforma'].nunique(),
        'categorias_unicas': df['categoria'].nunique(),
        'dias_comprando': (df['fecha'].max() - df['fecha'].min()).days
    }
    
    return resumen