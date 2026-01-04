"""
Módulo para crear visualizaciones gráficas
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

SIMBOLO_MONEDA = "$"

def crear_grafico_gasto_mensual(df_filtrado):
    """
    Crea gráfico de línea para gasto mensual
    """
    if df_filtrado.empty:
        return None
    
    # Agrupar por mes
    gasto_mensual = df_filtrado.groupby(['mes', 'mes_nombre'])['total_compra'].sum().reset_index()
    gasto_mensual = gasto_mensual.sort_values('mes')
    
    # Crear gráfico
    fig = px.line(
        gasto_mensual,
        x='mes_nombre',
        y='total_compra',
        markers=True,
        title="📅 Evolución del Gasto Mensual",
        labels={'mes_nombre': 'Mes', 'total_compra': f'Gasto Total ({SIMBOLO_MONEDA})'}
    )
    
    fig.update_layout(
        xaxis_title="Mes",
        yaxis_title=f"Gasto Total ({SIMBOLO_MONEDA})",
        hovermode='x unified'
    )
    
    return fig

def crear_grafico_plataformas(df_filtrado):
    """
    Crea gráfico circular para distribución por plataforma
    """
    if df_filtrado.empty:
        return None
    
    compras_plataforma = df_filtrado.groupby('plataforma').agg({
        'total_compra': 'sum',
        'producto': 'count'
    }).reset_index()
    
    compras_plataforma.columns = ['Plataforma', 'Gasto Total', 'Cantidad Compras']
    
    # Crear gráfico
    fig = px.pie(
        compras_plataforma,
        values='Gasto Total',
        names='Plataforma',
        title="🛒 Distribución del Gasto por Plataforma",
        hole=0.4
    )
    
    return fig

def crear_grafico_categorias(df_filtrado):
    """
    Crea gráfico de barras para gasto por categoría
    """
    if df_filtrado.empty:
        return None
    
    compras_categoria = df_filtrado.groupby('categoria').agg({
        'total_compra': 'sum',
        'producto': 'count'
    }).reset_index()
    
    compras_categoria.columns = ['Categoría', 'Gasto Total', 'Cantidad']
    compras_categoria = compras_categoria.sort_values('Gasto Total', ascending=False)
    
    # Crear gráfico
    fig = px.bar(
        compras_categoria,
        x='Categoría',
        y='Gasto Total',
        color='Categoría',
        title="🏷️ Gasto por Categoría",
        labels={'Gasto Total': f'Gasto Total ({SIMBOLO_MONEDA})', 'Categoría': 'Categoría'},
        text='Gasto Total'
    )
    
    fig.update_traces(
        texttemplate=f'{SIMBOLO_MONEDA}%{{text:,.0f}}',
        textposition='outside'
    )
    
    fig.update_layout(
        xaxis_title="Categoría",
        yaxis_title=f"Gasto Total ({SIMBOLO_MONEDA})",
        showlegend=False,
        xaxis={'categoryorder': 'total descending'}
    )
    
    return fig

def crear_grafico_tendencias(df_filtrado):
    """
    Crea gráfico de tendencias semanales
    """
    if df_filtrado.empty:
        return None
    
    # Agrupar por semana
    df_filtrado['semana'] = df_filtrado['fecha'].dt.strftime('%Y-%U')
    tendencias = df_filtrado.groupby('semana').agg({
        'total_compra': 'sum',
        'producto': 'count'
    }).reset_index()
    
    tendencias.columns = ['Semana', 'Gasto Total', 'Cantidad Compras']
    
    # Crear gráfico
    fig = go.Figure()
    
    # Línea de gasto
    fig.add_trace(go.Scatter(
        x=tendencias['Semana'],
        y=tendencias['Gasto Total'],
        mode='lines+markers',
        name='Gasto Total',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="📈 Tendencias Semanales de Compras",
        xaxis_title="Semana",
        yaxis_title=f"Gasto Total ({SIMBOLO_MONEDA})",
        hovermode='x unified'
    )
    
    return fig

def crear_grafico_distribucion_precios(df_filtrado):
    """
    Crea histograma de distribución de precios
    """
    if df_filtrado.empty:
        return None
    
    fig = px.histogram(
        df_filtrado,
        x='precio',
        nbins=20,
        title="📊 Distribución de Precios",
        labels={'precio': f'Precio ({SIMBOLO_MONEDA})', 'count': 'Cantidad de Productos'}
    )
    
    fig.update_layout(
        xaxis_title=f"Precio ({SIMBOLO_MONEDA})",
        yaxis_title="Cantidad de Productos"
    )
    
    return fig

def crear_grafico_top_productos(df_filtrado, top_n=10):
    """
    Crea gráfico de los productos más caros
    """
    if df_filtrado.empty:
        return None
    
    # Obtener los productos más caros
    top_productos = df_filtrado.nlargest(top_n, 'total_compra')[['producto', 'total_compra', 'plataforma']]
    
    # Acortar nombres de productos si son muy largos
    top_productos['producto_corto'] = top_productos['producto'].apply(
        lambda x: x[:30] + '...' if len(x) > 30 else x
    )
    
    # Crear gráfico
    fig = px.bar(
        top_productos,
        x='total_compra',
        y='producto_corto',
        color='plataforma',
        orientation='h',
        title=f"🏆 Top {top_n} Productos Más Caros",
        labels={'total_compra': f'Gasto Total ({SIMBOLO_MONEDA})', 'producto_corto': 'Producto'},
        text='total_compra'
    )
    
    fig.update_traces(
        texttemplate=f'{SIMBOLO_MONEDA}%{{text:,.0f}}',
        textposition='outside'
    )
    
    fig.update_layout(
        xaxis_title=f"Gasto Total ({SIMBOLO_MONEDA})",
        yaxis_title="Producto",
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig

def crear_grafico_heatmap_calendario(df_filtrado):
    """
    Crea heatmap de gasto por día de la semana y mes
    """
    if df_filtrado.empty:
        return None
    
    # Preparar datos para heatmap
    df_filtrado['dia_semana_num'] = df_filtrado['fecha'].dt.dayofweek
    df_filtrado['dia_semana_nombre'] = df_filtrado['fecha'].dt.day_name()
    df_filtrado['mes_num'] = df_filtrado['fecha'].dt.month
    
    heatmap_data = df_filtrado.pivot_table(
        values='total_compra',
        index='dia_semana_nombre',
        columns='mes_num',
        aggfunc='sum',
        fill_value=0
    )
    
    # Ordenar días de la semana
    dias_ordenados = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dias_espanol = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    heatmap_data = heatmap_data.reindex(dias_ordenados)
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'][:len(heatmap_data.columns)],
        y=dias_espanol,
        colorscale='Viridis',
        hovertemplate='Día: %{y}<br>Mes: %{x}<br>Gasto: ' + SIMBOLO_MONEDA + '%{z:,.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title="📅 Heatmap de Gasto por Día y Mes",
        xaxis_title="Mes",
        yaxis_title="Día de la Semana"
    )
    
    return fig