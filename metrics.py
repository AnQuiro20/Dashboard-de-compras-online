"""
Módulo para calcular y mostrar métricas
"""
import streamlit as st
import pandas as pd

SIMBOLO_MONEDA = "$"

def mostrar_metricas_principales(df_filtrado):
    """
    Muestra las métricas principales en 4 columnas
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_compras = len(df_filtrado)
        st.metric("📦 Total de Compras", total_compras)
    
    with col2:
        monto_total = df_filtrado['total_compra'].sum()
        st.metric("💰 Monto Total Gastado", f"{SIMBOLO_MONEDA}{monto_total:,.2f}")
    
    with col3:
        if not df_filtrado.empty:
            compra_cara = df_filtrado.loc[df_filtrado['total_compra'].idxmax()]
            producto_caro = compra_cara['producto'][:20] + "..." if len(compra_cara['producto']) > 20 else compra_cara['producto']
            st.metric("🏆 Compra más Cara", 
                     f"{SIMBOLO_MONEDA}{compra_cara['total_compra']:,.2f}",
                     delta=producto_caro)
        else:
            st.metric("🏆 Compra más Cara", f"{SIMBOLO_MONEDA}0.00")
    
    with col4:
        if not df_filtrado.empty:
            compra_barata = df_filtrado.loc[df_filtrado['total_compra'].idxmin()]
            producto_barato = compra_barata['producto'][:20] + "..." if len(compra_barata['producto']) > 20 else compra_barata['producto']
            st.metric("🎯 Compra más Barata", 
                     f"{SIMBOLO_MONEDA}{compra_barata['total_compra']:,.2f}",
                     delta=producto_barato)
        else:
            st.metric("🎯 Compra más Barata", f"{SIMBOLO_MONEDA}0.00")

def mostrar_metricas_secundarias(df_filtrado):
    """
    Muestra métricas secundarias
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not df_filtrado.empty:
            promedio_compra = df_filtrado['total_compra'].mean()
            st.metric("📊 Gasto Promedio", f"{SIMBOLO_MONEDA}{promedio_compra:,.2f}")
        else:
            st.metric("📊 Gasto Promedio", f"{SIMBOLO_MONEDA}0.00")
    
    with col2:
        if not df_filtrado.empty:
            plataformas_unicas = df_filtrado['plataforma'].nunique()
            st.metric("🛒 Plataformas", plataformas_unicas)
        else:
            st.metric("🛒 Plataformas", 0)
    
    with col3:
        if not df_filtrado.empty:
            categorias_unicas = df_filtrado['categoria'].nunique()
            st.metric("🏷️ Categorías", categorias_unicas)
        else:
            st.metric("🏷️ Categorías", 0)
    
    with col4:
        if not df_filtrado.empty:
            dias_comprando = (df_filtrado['fecha'].max() - df_filtrado['fecha'].min()).days
            st.metric("📅 Días de Compras", dias_comprando)
        else:
            st.metric("📅 Días de Compras", 0)

def mostrar_resumen_estadistico(df_filtrado):
    """
    Muestra un resumen estadístico detallado
    """
    st.subheader("📋 Resumen Estadístico Detallado")
    
    if df_filtrado.empty:
        st.warning("No hay datos para mostrar estadísticas.")
        return
    
    # Estadísticas por plataforma
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Por Plataforma")
        plataforma_stats = df_filtrado.groupby('plataforma').agg({
            'total_compra': ['sum', 'mean', 'count', 'max', 'min']
        }).round(2)
        
        # Renombrar columnas
        plataforma_stats.columns = ['Total', 'Promedio', 'Cantidad', 'Máximo', 'Mínimo']
        
        # Formatear valores
        for col in ['Total', 'Promedio', 'Máximo', 'Mínimo']:
            plataforma_stats[col] = plataforma_stats[col].apply(lambda x: f"{SIMBOLO_MONEDA}{x:,.2f}")
        
        # CORREGIDO
        st.dataframe(plataforma_stats, width='stretch')
    
    with col2:
        st.subheader("🏷️ Por Categoría")
        categoria_stats = df_filtrado.groupby('categoria').agg({
            'total_compra': ['sum', 'mean', 'count']
        }).round(2)
        
        # Renombrar columnas
        categoria_stats.columns = ['Total', 'Promedio', 'Cantidad']
        
        # Formatear valores
        for col in ['Total', 'Promedio']:
            categoria_stats[col] = categoria_stats[col].apply(lambda x: f"{SIMBOLO_MONEDA}{x:,.2f}")
        
        # CORREGIDO
        st.dataframe(categoria_stats, width='stretch')
    
    # Estadísticas generales
    st.subheader("📈 Estadísticas Generales")
    
    general_stats = {
        'Total de Compras': len(df_filtrado),
        'Monto Total Gastado': f"{SIMBOLO_MONEDA}{df_filtrado['total_compra'].sum():,.2f}",
        'Gasto Promedio por Compra': f"{SIMBOLO_MONEDA}{df_filtrado['total_compra'].mean():,.2f}",
        'Mediana de Gasto': f"{SIMBOLO_MONEDA}{df_filtrado['total_compra'].median():,.2f}",
        'Desviación Estándar': f"{SIMBOLO_MONEDA}{df_filtrado['total_compra'].std():,.2f}",
        'Primera Compra': df_filtrado['fecha'].min().strftime('%Y-%m-%d'),
        'Última Compra': df_filtrado['fecha'].max().strftime('%Y-%m-%d'),
        'Días entre Compras': f"{(df_filtrado['fecha'].max() - df_filtrado['fecha'].min()).days} días",
        'Plataformas Diferentes': df_filtrado['plataforma'].nunique(),
        'Categorías Diferentes': df_filtrado['categoria'].nunique(),
        'Productos Diferentes': df_filtrado['producto'].nunique()
    }
    
    # Mostrar en columnas
    cols = st.columns(3)
    for idx, (key, value) in enumerate(general_stats.items()):
        with cols[idx % 3]:
            st.metric(key, value)