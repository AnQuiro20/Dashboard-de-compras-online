"""
Módulo para análisis automático de insights y recomendaciones
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

SIMBOLO_MONEDA = "$"

def generar_insight_gasto_mensual(df):
    """Genera insight sobre patrones de gasto mensual"""
    if df.empty:
        return []
    
    insights = []
    
    # Agrupar por mes
    gasto_mensual = df.groupby('mes')['total_compra'].sum().reset_index()
    gasto_mensual = gasto_mensual.sort_values('mes')
    
    if len(gasto_mensual) > 1:
        # Calcular tendencia
        gasto_mensual['diferencia'] = gasto_mensual['total_compra'].diff()
        crecimiento_promedio = gasto_mensual['diferencia'].mean()
        
        # Último mes vs penúltimo mes
        ultimo_mes = gasto_mensual.iloc[-1]['total_compra']
        penultimo_mes = gasto_mensual.iloc[-2]['total_compra'] if len(gasto_mensual) > 1 else 0
        
        if crecimiento_promedio > 0:
            insights.append(f"📈 **Tendencia alcista**: Tu gasto mensual está aumentando en promedio {SIMBOLO_MONEDA}{abs(crecimiento_promedio):,.2f} por mes")
        elif crecimiento_promedio < 0:
            insights.append(f"📉 **Tendencia bajista**: Tu gasto mensual está disminuyendo en promedio {SIMBOLO_MONEDA}{abs(crecimiento_promedio):,.2f} por mes")
        else:
            insights.append("📊 **Estabilidad**: Tu gasto mensual se mantiene constante")
        
        # Mes con mayor gasto
        mes_max = gasto_mensual.loc[gasto_mensual['total_compra'].idxmax()]
        insights.append(f"💰 **Mes pico**: {mes_max['mes']} fue el mes con mayor gasto ({SIMBOLO_MONEDA}{mes_max['total_compra']:,.2f})")
    
    return insights

def generar_insight_plataformas(df):
    """Genera insights sobre patrones por plataforma"""
    if df.empty:
        return []
    
    insights = []
    
    # Análisis por plataforma
    plataforma_stats = df.groupby('plataforma').agg({
        'total_compra': 'sum',
        'producto': 'count',
        'precio': 'mean'
    }).round(2)
    
    plataforma_stats = plataforma_stats.sort_values('total_compra', ascending=False)
    
    # Plataforma favorita (más gasto)
    plataforma_top = plataforma_stats.index[0]
    gasto_top = plataforma_stats.iloc[0]['total_compra']
    porcentaje_top = (gasto_top / df['total_compra'].sum()) * 100
    
    insights.append(f"🏆 **Plataforma principal**: {plataforma_top} representa el {porcentaje_top:.1f}% de tu gasto total ({SIMBOLO_MONEDA}{gasto_top:,.2f})")
    
    # Plataforma con compras más frecuentes
    plataforma_frecuente = plataforma_stats.sort_values('producto', ascending=False).index[0]
    compras_frecuentes = plataforma_stats.sort_values('producto', ascending=False).iloc[0]['producto']
    
    insights.append(f"🛒 **Plataforma frecuente**: {plataforma_frecuente} con {compras_frecuentes} compras realizadas")
    
    return insights

def generar_insight_categorias(df):
    """Genera insights sobre patrones por categoría"""
    if df.empty:
        return []
    
    insights = []
    
    # Análisis por categoría
    categoria_stats = df.groupby('categoria').agg({
        'total_compra': 'sum',
        'producto': 'count'
    }).round(2)
    
    categoria_stats = categoria_stats.sort_values('total_compra', ascending=False)
    
    # Categoría con mayor gasto
    categoria_top = categoria_stats.index[0]
    gasto_categoria_top = categoria_stats.iloc[0]['total_compra']
    porcentaje_categoria = (gasto_categoria_top / df['total_compra'].sum()) * 100
    
    insights.append(f"📦 **Categoría principal**: {categoria_top} absorbe el {porcentaje_categoria:.1f}% de tu presupuesto ({SIMBOLO_MONEDA}{gasto_categoria_top:,.2f})")
    
    # Diversidad de categorías
    num_categorias = len(categoria_stats)
    if num_categorias >= 5:
        insights.append(f"🌈 **Diversificación**: Compras en {num_categorias} categorías diferentes, buena variedad")
    elif num_categorias >= 3:
        insights.append(f"🎯 **Enfoque moderado**: Compras en {num_categorias} categorías principales")
    else:
        insights.append(f"🎯 **Alto enfoque**: Concentras tus compras en solo {num_categorias} categorías")
    
    return insights

def generar_insight_temporal(df):
    """Genera insights sobre patrones temporales"""
    if df.empty:
        return []
    
    insights = []
    
    # Día de la semana preferido
    df['dia_semana'] = df['fecha'].dt.day_name()
    dias_semana_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dias_espanol = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    
    compras_por_dia = df.groupby('dia_semana')['total_compra'].sum().reindex(dias_semana_orden)
    dia_max = compras_por_dia.idxmax()
    gasto_dia_max = compras_por_dia.max()
    
    # Mapear a español
    dia_espanol = dias_espanol[dias_semana_orden.index(dia_max)]
    
    insights.append(f"📅 **Día preferido**: {dia_espanol} es cuando más gastas ({SIMBOLO_MONEDA}{gasto_dia_max:,.2f})")
    
    return insights

def generar_recomendaciones(df):
    """Genera recomendaciones basadas en los datos"""
    if df.empty:
        return []
    
    recomendaciones = []
    
    # 1. Recomendación basada en gasto por plataforma
    plataforma_stats = df.groupby('plataforma')['total_compra'].sum()
    if len(plataforma_stats) > 1:
        plataforma_max = plataforma_stats.idxmax()
        plataforma_min = plataforma_stats.idxmin()
        
        if plataforma_stats.max() / plataforma_stats.min() > 5:  # Si hay mucha diferencia
            recomendaciones.append(f"⚖️ **Considera diversificar**: {plataforma_max} representa una gran parte de tu gasto. Podrías explorar más opciones en {plataforma_min}")
    
    # 2. Recomendación basada en categorías
    categoria_stats = df.groupby('categoria')['total_compra'].sum()
    if len(categoria_stats) < 3:
        recomendaciones.append("🛍️ **Amplía tus categorías**: Estás comprando en pocas categorías. Considera explorar nuevas áreas de interés")
    
    # 3. Recomendación basada en frecuencia
    df_sorted = df.sort_values('fecha')
    frecuencia_promedio = df_sorted['fecha'].diff().dt.days.mean()
    
    if frecuencia_promedio < 3:
        recomendaciones.append("⏰ **Control de impulsos**: Compras con mucha frecuencia. Considera esperar 24h antes de compras no esenciales")
    elif frecuencia_promedio > 30:
        recomendaciones.append("🎯 **Planificación**: Compras con poca frecuencia. Podrías planificar compras mayores para ahorrar en envíos")
    
    return recomendaciones

def generar_alertas(df):
    """Genera alertas importantes basadas en los datos"""
    if df.empty:
        return []
    
    alertas = []
    
    # 1. Alerta de gasto excesivo reciente
    ultimo_mes = df['fecha'].max()
    hace_30_dias = ultimo_mes - timedelta(days=30)
    compras_recientes = df[df['fecha'] >= hace_30_dias]
    
    if not compras_recientes.empty:
        gasto_reciente = compras_recientes['total_compra'].sum()
        gasto_promedio_mensual = df['total_compra'].sum() / (len(df) / 30)  # Aproximación
        
        if gasto_reciente > gasto_promedio_mensual * 1.5:
            alertas.append(f"🚨 **Gasto elevado reciente**: En los últimos 30 días gastaste {SIMBOLO_MONEDA}{gasto_reciente:,.2f}, mucho más que tu promedio mensual")
    
    # 2. Alerta de compras repetitivas
    productos_frecuentes = df['producto'].value_counts()
    if productos_frecuentes.max() >= 3:
        producto_repetido = productos_frecuentes.idxmax()
        alertas.append(f"🔄 **Producto repetido**: '{producto_repetido}' lo has comprado {productos_frecuentes.max()} veces")
    
    return alertas

def mostrar_insights_generales(df):
    """Muestra todos los insights generales"""
    st.subheader("📊 Insights Generales")
    
    # Obtener todos los insights
    todos_insights = []
    todos_insights.extend(generar_insight_gasto_mensual(df))
    todos_insights.extend(generar_insight_plataformas(df))
    todos_insights.extend(generar_insight_categorias(df))
    todos_insights.extend(generar_insight_temporal(df))
    
    # Mostrar en tarjetas
    for insight in todos_insights:
        st.info(insight)

def mostrar_patrones_compras(df):
    """Muestra patrones detectados en las compras"""
    
    # Patrón 1: Día preferido de compras
    df['dia_semana'] = df['fecha'].dt.day_name()
    dias_semana_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dias_espanol = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    
    compras_por_dia = df.groupby('dia_semana')['total_compra'].sum().reindex(dias_semana_orden, fill_value=0)
    
    if not compras_por_dia.empty:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            dia_max = compras_por_dia.idxmax()
            dia_espanol_max = dias_espanol[dias_semana_orden.index(dia_max)]
            st.metric("📅 Día preferido", dia_espanol_max)
        
        with col2:
            # Frecuencia de compras
            df_sorted = df.sort_values('fecha')
            frecuencia = df_sorted['fecha'].diff().dt.days.mean()
            st.metric("⏰ Frecuencia", f"{frecuencia:.1f} días")
        
        with col3:
            st.metric("🛒 Compras totales", len(df))

def mostrar_recomendaciones(df):
    """Muestra recomendaciones personalizadas"""
    
    recomendaciones = generar_recomendaciones(df)
    
    if recomendaciones:
        for rec in recomendaciones:
            st.success(f"{rec}")
    else:
        st.info("Tus hábitos de compra parecen balanceados. ¡Sigue así!")

def mostrar_alertas_oportunidades(df):
    """Muestra alertas y oportunidades"""
    
    alertas = generar_alertas(df)
    
    if alertas:
        for alerta in alertas:
            if "🚨" in alerta:
                st.error(alerta)
            else:
                st.warning(alerta)
    else:
        st.success("✅ No se detectaron alertas críticas en tus patrones de compra")