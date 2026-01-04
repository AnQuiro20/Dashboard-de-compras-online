"""
Dashboard de Compras Online - Archivo principal
"""
import streamlit as st
from data_loader import *
from metrics import *
from charts import *
from insights import *

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Compras Online",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título del dashboard
st.title("🛒 Dashboard de Compras Online")
st.markdown("Analiza tus hábitos de gasto en diferentes plataformas de comercio electrónico")

# Sidebar para filtros
st.sidebar.header("🔍 Filtros")

# Subir archivo personalizado
archivo_subido = st.sidebar.file_uploader("Subir archivo JSON o CSV", type=['json', 'csv'])

# Cargar datos
if archivo_subido:
    df = cargar_datos_subidos(archivo_subido)
else:
    df = cargar_datos('compras.json')

if df.empty:
    st.warning("No hay datos para mostrar. Por favor, sube un archivo o verifica 'compras.json'.")
    st.stop()

# Obtener opciones para filtros
plataformas, categorias = obtener_opciones_filtros(df)

# Filtro por plataforma
plataforma_seleccionada = st.sidebar.selectbox("Seleccionar Plataforma", plataformas)

# Filtro por categoría
categoria_seleccionada = st.sidebar.selectbox("Seleccionar Categoría", categorias)

# Filtro por rango de fechas
fecha_min = df['fecha'].min().date()
fecha_max = df['fecha'].max().date()
rango_fechas = st.sidebar.date_input("Rango de Fechas", [fecha_min, fecha_max])

# Aplicar filtros
df_filtrado = aplicar_filtros(df, plataforma_seleccionada, categoria_seleccionada, rango_fechas)

# Sección principal del dashboard
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Resumen", "📈 Gráficos", "📋 Detalles", "⚙️ Análisis", "🤖 Insight Automático"])

with tab1:
    # Métricas principales
    st.header("📊 Métricas Principales")
    mostrar_metricas_principales(df_filtrado)
    
    st.markdown("---")
    
    # Métricas secundarias
    st.header("📈 Métricas Secundarias")
    mostrar_metricas_secundarias(df_filtrado)
    
    # Resumen estadístico
    mostrar_resumen_estadistico(df_filtrado)

with tab2:
    st.header("📈 Visualizaciones Gráficas")
    
    # Gráficos básicos
    col1, col2 = st.columns(2)
    
    with col1:
        fig_mensual = crear_grafico_gasto_mensual(df_filtrado)
        if fig_mensual:
            # CORREGIDO: Sin use_container_width
            st.plotly_chart(fig_mensual)
    
    with col2:
        fig_plataformas = crear_grafico_plataformas(df_filtrado)
        if fig_plataformas:
            # CORREGIDO: Sin use_container_width
            st.plotly_chart(fig_plataformas)
    
    # Gráfico de categorías
    fig_categorias = crear_grafico_categorias(df_filtrado)
    if fig_categorias:
        # CORREGIDO: Sin use_container_width
        st.plotly_chart(fig_categorias)
    
    # Gráficos avanzados
    st.subheader("📊 Gráficos Avanzados")
    col3, col4 = st.columns(2)
    
    with col3:
        fig_tendencias = crear_grafico_tendencias(df_filtrado)
        if fig_tendencias:
            # CORREGIDO: Sin use_container_width
            st.plotly_chart(fig_tendencias)
    
    with col4:
        fig_distribucion = crear_grafico_distribucion_precios(df_filtrado)
        if fig_distribucion:
            # CORREGIDO: Sin use_container_width
            st.plotly_chart(fig_distribucion)

with tab3:
    st.header("📋 Detalle de Compras")
    
    if not df_filtrado.empty:
        # Formatear tabla para mostrar
        df_mostrar = df_filtrado.copy()
        df_mostrar['fecha'] = df_mostrar['fecha'].dt.strftime('%Y-%m-%d')
        df_mostrar['precio'] = df_mostrar['precio'].apply(lambda x: f"{SIMBOLO_MONEDA}{x:,.2f}")
        df_mostrar['total_compra'] = df_mostrar['total_compra'].apply(lambda x: f"{SIMBOLO_MONEDA}{x:,.2f}")
        
        # Renombrar columnas
        df_mostrar = df_mostrar.rename(columns={
            'fecha': 'Fecha',
            'plataforma': 'Plataforma',
            'producto': 'Producto',
            'categoria': 'Categoría',
            'cantidad': 'Cantidad',
            'precio': 'Precio Unitario',
            'total_compra': 'Total Compra'
        })
        
        # CORREGIDO: width='stretch' en lugar de use_container_width
        st.dataframe(df_mostrar, hide_index=True, width='stretch')
        
        # Opción para descargar - CORREGIDO
        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar datos filtrados (CSV)",
            data=csv,
            file_name="compras_filtradas.csv",
            mime="text/csv",
            width='stretch'
        )
    else:
        st.warning("No hay datos que coincidan con los filtros seleccionados")

with tab4:
    st.header("⚙️ Análisis Avanzado")
    
    if not df_filtrado.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📅 Heatmap de Gasto")
            fig_heatmap = crear_grafico_heatmap_calendario(df_filtrado)
            if fig_heatmap:
                # CORREGIDO: Sin use_container_width
                st.plotly_chart(fig_heatmap)
        
        with col2:
            st.subheader("🏆 Top Productos")
            fig_top = crear_grafico_top_productos(df_filtrado, top_n=10)
            if fig_top:
                # CORREGIDO: Sin use_container_width
                st.plotly_chart(fig_top)
    else:
        st.warning("No hay datos para análisis avanzado")

# NUEVA PESTAÑA: Insight Automático
with tab5:
    st.header("🤖 Insight Automático")
    st.markdown("Análisis inteligente automatizado de tus patrones de compra")
    
    if not df_filtrado.empty:
        # Mostrar insights automáticos
        mostrar_insights_generales(df_filtrado)
        
        st.markdown("---")
        
        # Análisis de patrones
        st.subheader("🔍 Análisis de Patrones Detectados")
        mostrar_patrones_compras(df_filtrado)
        
        st.markdown("---")
        
        # Recomendaciones personalizadas
        st.subheader("💡 Recomendaciones Personalizadas")
        mostrar_recomendaciones(df_filtrado)
        
        st.markdown("---")
        
        # Alertas y oportunidades
        st.subheader("🚨 Alertas y Oportunidades")
        mostrar_alertas_oportunidades(df_filtrado)
        
    else:
        st.warning("No hay datos suficientes para generar insights automáticos")

# Información en el sidebar
st.sidebar.markdown("---")
st.sidebar.info("""
**Dashboard de Compras Online**

Este dashboard te permite:
- Analizar tus hábitos de compra
- Comparar gastos entre plataformas
- Identificar tendencias de consumo
- Exportar datos filtrados
- **Nuevo:** Insight automático con IA
""")

# Pie de página
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    Dashboard de Compras Online • Desarrollado con Streamlit • 🤖 Insight Automático
    </div>
    """,
    unsafe_allow_html=True
)