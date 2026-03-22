"""
Rendering Components for Bot Responses
Modular components to display different response types
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from schemas import BotResponse, ChartData, InsightCard
from typing import List, Optional


class ResponseRenderer:
    """Renders different types of bot responses"""
    
    @staticmethod
    def render_text(text: str) -> None:
        """Render plain text response"""
        st.markdown(text)
    
    @staticmethod
    def render_insights(insights: List[InsightCard]) -> None:
        """Render insight cards in columns"""
        if not insights:
            return
        
        # Dynamic column layout (3-4 cards per row)
        cols = st.columns(min(len(insights), 4))
        
        for idx, insight in enumerate(insights):
            col = cols[idx % len(cols)]
            with col:
                render_insight_card(insight)
    
    @staticmethod
    def render_charts(charts: List[ChartData]) -> None:
        """Render charts (one or two per row)"""
        if not charts:
            return
        
        for i in range(0, len(charts), 2):
            if i + 1 < len(charts):
                # Two charts per row
                col1, col2 = st.columns(2)
                with col1:
                    ResponseRenderer.render_single_chart(charts[i])
                with col2:
                    ResponseRenderer.render_single_chart(charts[i + 1])
            else:
                # Single chart
                ResponseRenderer.render_single_chart(charts[i])
    
    @staticmethod
    def render_single_chart(chart: ChartData) -> None:
        """Render a single chart based on type"""
        if chart.type == "line":
            render_line_chart(chart.data, chart.title)
        elif chart.type == "bar":
            render_bar_chart(chart.data, chart.title)
        elif chart.type == "area":
            render_area_chart(chart.data, chart.title)
        elif chart.type == "scatter":
            render_scatter_chart(chart.data, chart.title)
        elif chart.type == "gauge":
            render_gauge_chart(chart.data, chart.title)
        else:
            st.warning(f"Chart type '{chart.type}' not yet supported")
    
    @staticmethod
    def render_recommendations(recommendations: List[str]) -> None:
        """Render recommendations as a bulleted list"""
        if not recommendations:
            return
        
        st.markdown("### 💡 Recommendations")
        for rec in recommendations:
            st.markdown(f"• {rec}")
    
    @staticmethod
    def render_alert(alert: dict) -> None:
        """Render alert message"""
        if not alert:
            return
        
        alert_type = alert.get("type", "info")
        message = alert.get("message", "")
        
        if alert_type == "error":
            st.error(message)
        elif alert_type == "warning":
            st.warning(message)
        elif alert_type == "success":
            st.success(message)
        else:
            st.info(message)
    
    @staticmethod
    def render_full_response(response: BotResponse) -> None:
        """Render complete bot response"""
        # Alert (if present)
        if response.alert:
            ResponseRenderer.render_alert(response.alert)
            st.divider()
        
        # Main text
        if response.text:
            ResponseRenderer.render_text(response.text)
        
        # Insights
        if response.insights:
            st.markdown("---")
            ResponseRenderer.render_insights(response.insights)
        
        # Charts
        if response.charts:
            st.markdown("---")
            ResponseRenderer.render_charts(response.charts)
        
        # Recommendations
        if response.recommendations:
            st.markdown("---")
            ResponseRenderer.render_recommendations(response.recommendations)


def render_insight_card(insight: InsightCard) -> None:
    """Render a single insight card - Data-focused and serious"""
    # Color mapping - One accent color per card, high contrast
    color_map = {
        "green": "#10B981",     # Emerald
        "red": "#EF4444",       # Red
        "orange": "#F97316",    # Orange
        "blue": "#3B82F6",      # Blue
        "yellow": "#FBBF24",    # Amber
        "purple": "#A855F7",    # Purple
    }
    
    color = color_map.get(insight.color or "blue", "#3B82F6")
    
    # Create styled metric card - Number-first hierarchy
    html_content = f"""
    <div style="
        padding: 20px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 6px;
        margin-bottom: 10px;
        transition: background 0.2s ease, border-color 0.2s ease;
    ">
        <div style="
            font-size: 28px; 
            font-weight: 700; 
            color: {color};
            letter-spacing: -0.7px;
            line-height: 1.1;
            margin-bottom: 6px;
        ">
            {insight.value}<span style="font-size: 16px; font-weight: 500; opacity: 0.8; margin-left: 4px;">{insight.unit or ''}</span>
        </div>
        <div style="
            font-size: 12px; 
            color: #CBD5E1;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 500;
            opacity: 0.8;
            margin-bottom: 8px;
        ">
            {insight.label}
        </div>
        {render_trend_indicator(insight.trend) if insight.trend else ''}
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)


def render_trend_indicator(trend: Optional[str]) -> str:
    """Render trend indicator - Subtle inline"""
    if trend == "up":
        return '<div style="font-size: 11px; color: #10B981; font-weight: 500; opacity: 0.85;">📈 Increasing</div>'
    elif trend == "down":
        return '<div style="font-size: 11px; color: #F97316; font-weight: 500; opacity: 0.85;">📉 Decreasing</div>'
    elif trend == "stable":
        return '<div style="font-size: 11px; color: #3B82F6; font-weight: 500; opacity: 0.85;">➡️ Stable</div>'
    return ""


def render_line_chart(data: dict, title: str) -> None:
    """Render line chart using Plotly - Premium dark theme"""
    fig = go.Figure()
    
    x = data.get("x", [])
    y = data.get("y", [])
    name = data.get("name", "Value")
    
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines+markers',
        name=name,
        line=dict(color='#3B82F6', width=2.5),
        marker=dict(size=6, color='#3B82F6', line=dict(width=1, color='#1E293B')),
        hovertemplate='<b>%{x}</b><br>%{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color='#F1F5F9', family='system-ui', weight=600)),
        xaxis_title="",
        yaxis_title="",
        hovermode='x unified',
        height=320,
        template="plotly_dark",
        showlegend=False,
        paper_bgcolor='rgba(30, 41, 59, 0.6)',
        plot_bgcolor='rgba(15, 23, 42, 0.3)',
        margin=dict(t=50, b=30, l=50, r=20),
        xaxis=dict(
            gridcolor='rgba(71, 85, 105, 0.15)',
            showgrid=True,
            zeroline=False,
            tickfont=dict(size=11, color='#94A3B8'),
            showline=True,
            linewidth=1,
            linecolor='rgba(71, 85, 105, 0.4)',
            mirror=True
        ),
        yaxis=dict(
            gridcolor='rgba(71, 85, 105, 0.15)',
            showgrid=True,
            zeroline=False,
            tickfont=dict(size=11, color='#94A3B8'),
            showline=True,
            linewidth=1,
            linecolor='rgba(71, 85, 105, 0.4)',
            mirror=True
        ),
    )
    
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_bar_chart(data: dict, title: str) -> None:
    """Render bar chart - Dark mode optimized for readability"""
    fig = go.Figure()
    
    # Handle different data formats
    x = data.get("x") or data.get("crops", [])
    y = data.get("y") or data.get("score", [])
    name = data.get("name", "Value")
    
    fig.add_trace(go.Bar(
        x=x, y=y,
        name=name,
        marker=dict(color='#3B82F6', line=dict(color='rgba(71, 85, 105, 0.3)', width=1)),
        hovertemplate='<b>%{x}</b><br>%{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color='#F1F5F9', family='system-ui', weight=600)),
        xaxis_title="",
        yaxis_title="",
        hovermode='x',
        height=320,
        template="plotly_dark",
        showlegend=False,
        paper_bgcolor='rgba(30, 41, 59, 0.6)',
        plot_bgcolor='rgba(15, 23, 42, 0.3)',
        margin=dict(t=50, b=40, l=50, r=20),
        xaxis=dict(
            gridcolor='rgba(71, 85, 105, 0.15)',
            showgrid=False,
            zeroline=False,
            tickfont=dict(size=11, color='#94A3B8'),
            showline=True,
            linewidth=1,
            linecolor='rgba(71, 85, 105, 0.4)',
            mirror=True
        ),
        yaxis=dict(
            gridcolor='rgba(71, 85, 105, 0.15)',
            showgrid=True,
            zeroline=False,
            tickfont=dict(size=11, color='#94A3B8'),
            showline=True,
            linewidth=1,
            linecolor='rgba(71, 85, 105, 0.4)',
            mirror=True
        ),
    )
    
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_area_chart(data: dict, title: str) -> None:
    """Render area chart - Dark mode optimized for readability"""
    fig = go.Figure()
    
    x = data.get("x", [])
    
    colors = ['#3B82F6', '#60A5FA', '#93C5FD']
    idx = 0
    
    for key in ["nitrogen", "phosphorus", "potassium"]:
        if key in data:
            fig.add_trace(go.Scatter(
                x=x, y=data[key],
                mode='lines',
                name=key.capitalize(),
                stackgroup='one',
                line=dict(width=0.5, color=colors[idx]),
                fillcolor=colors[idx],
                hovertemplate='<b>' + key.capitalize() + '</b><br>%{y}<extra></extra>'
            ))
            idx += 1
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color='#F1F5F9', family='system-ui', weight=600)),
        xaxis_title="",
        yaxis_title="",
        hovermode='x unified',
        height=320,
        template="plotly_dark",
        paper_bgcolor='rgba(30, 41, 59, 0.6)',
        plot_bgcolor='rgba(15, 23, 42, 0.3)',
        margin=dict(t=50, b=30, l=50, r=20),
        xaxis=dict(
            gridcolor='rgba(71, 85, 105, 0.15)',
            showgrid=True,
            zeroline=False,
            tickfont=dict(size=11, color='#94A3B8'),
            showline=True,
            linewidth=1,
            linecolor='rgba(71, 85, 105, 0.4)',
            mirror=True
        ),
        yaxis=dict(
            gridcolor='rgba(71, 85, 105, 0.15)',
            showgrid=True,
            zeroline=False,
            tickfont=dict(size=11, color='#94A3B8'),
            showline=True,
            linewidth=1,
            linecolor='rgba(71, 85, 105, 0.4)',
            mirror=True
        ),
    )
    
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_scatter_chart(data: dict, title: str) -> None:
    """Render scatter chart - Dark mode optimized for readability"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data.get("x", []),
        y=data.get("y", []),
        mode='markers',
        marker=dict(size=8, color='#3B82F6', line=dict(width=1, color='rgba(71, 85, 105, 0.3)')),
        hovertemplate='<b>X: %{x}</b><br><b>Y: %{y}</b><extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color='#F1F5F9', family='system-ui', weight=600)),
        xaxis_title="",
        yaxis_title="",
        height=320,
        template="plotly_dark",
        showlegend=False,
        paper_bgcolor='rgba(30, 41, 59, 0.6)',
        plot_bgcolor='rgba(15, 23, 42, 0.3)',
        margin=dict(t=50, b=30, l=50, r=20),
        xaxis=dict(
            gridcolor='rgba(71, 85, 105, 0.15)',
            showgrid=True,
            zeroline=False,
            tickfont=dict(size=11, color='#94A3B8'),
            showline=True,
            linewidth=1,
            linecolor='rgba(71, 85, 105, 0.4)',
            mirror=True
        ),
        yaxis=dict(
            gridcolor='rgba(71, 85, 105, 0.15)',
            showgrid=True,
            zeroline=False,
            tickfont=dict(size=11, color='#94A3B8'),
            showline=True,
            linewidth=1,
            linecolor='rgba(71, 85, 105, 0.4)',
            mirror=True
        ),
    )
    
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_gauge_chart(data: dict, title: str) -> None:
    """Render gauge chart - Dark mode optimized for readability"""
    value = data.get("value", 50)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={'text': title, 'font': {'size': 14, 'color': '#F1F5F9', 'family': 'system-ui', 'weight': 600}},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#94A3B8', 'tickfont': {'size': 11}, 'tickwidth': 1},
            'bar': {'color': "#3B82F6", 'thickness': 12},
            'bgcolor': "rgba(15, 23, 42, 0.3)",
            'borderwidth': 1,
            'bordercolor': 'rgba(71, 85, 105, 0.3)',
            'steps': [
                {'range': [0, 33], 'color': "rgba(239, 68, 68, 0.12)"},
                {'range': [33, 66], 'color': "rgba(249, 115, 22, 0.12)"},
                {'range': [66, 100], 'color': "rgba(16, 185, 129, 0.12)"}
            ]
        },
        number={'font': {'size': 28, 'color': '#F1F5F9', 'family': 'system-ui'}},
    ))
    
    fig.update_layout(
        height=340,
        template="plotly_dark",
        paper_bgcolor='rgba(30, 41, 59, 0.6)',
        margin=dict(t=50, b=30, l=40, r=40),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
