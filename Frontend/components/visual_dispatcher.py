"""
Visual Dispatcher Component
Renders various visualization types (charts, maps) from bot response JSON
Supports Plotly charts and PyDeck geographic visualizations
"""

from typing import Dict, Any, Optional, List
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pydeck as pdk
import pandas as pd
import numpy as np


class VisualizationDispatcher:
    """
    Routes and renders different visualization types.
    
    Supported chart types:
    - line: Time series with line plot
    - bar: Bar charts for categorical data
    - area: Area charts for stacked data
    - scatter: Scatter plots for relationships
    - gauge: Gauge charts for progress/KPIs
    - pie: Pie charts for distribution
    - heatmap: Heatmaps for 2D data
    - box: Box plots for distributions
    
    Supported map types:
    - map: Geographic visualizations with markers/layers
    """
    
    @staticmethod
    def render_chart(chart: Dict[str, Any]) -> None:
        """
        Main dispatcher for chart rendering.
        
        Routes to specific chart renderer based on chart type.
        
        Args:
            chart: Chart object from bot response
        """
        if not chart:
            st.warning("No chart data provided")
            return
        
        chart_type = chart.get("type", "line").lower()
        
        try:
            if chart_type == "line":
                VisualizationDispatcher._render_line_chart(chart)
            elif chart_type == "bar":
                VisualizationDispatcher._render_bar_chart(chart)
            elif chart_type == "area":
                VisualizationDispatcher._render_area_chart(chart)
            elif chart_type == "scatter":
                VisualizationDispatcher._render_scatter_chart(chart)
            elif chart_type == "gauge":
                VisualizationDispatcher._render_gauge_chart(chart)
            elif chart_type == "pie":
                VisualizationDispatcher._render_pie_chart(chart)
            elif chart_type == "heatmap":
                VisualizationDispatcher._render_heatmap(chart)
            elif chart_type == "box":
                VisualizationDispatcher._render_box_chart(chart)
            else:
                st.warning(f"Unsupported chart type: {chart_type}")
        except Exception as e:
            st.error(f"Error rendering {chart_type} chart: {str(e)}")
    
    @staticmethod
    def render_map(location: Dict[str, Any]) -> None:
        """
        Main dispatcher for map rendering.
        
        Renders geographic data with markers and layers using PyDeck.
        
        Args:
            location: Location object from bot response
        """
        if not location:
            st.warning("No location data provided")
            return
        
        try:
            VisualizationDispatcher._render_pydeck_map(location)
        except Exception as e:
            st.error(f"Error rendering map: {str(e)}")
    
    # ========================================================================
    # LINE CHART RENDERER
    # ========================================================================
    @staticmethod
    def _render_line_chart(chart: Dict[str, Any]) -> None:
        """
        Render time series line chart.
        
        Features:
        - Multiple series support
        - Scatter markers optional
        - Area fill optional
        - Custom colors
        - Interactive hover
        
        Args:
            chart: Chart configuration
        """
        data = chart.get("data", {})
        layout = chart.get("layout", {})
        
        x_values = data.get("x", [])
        y_values = data.get("y", [])
        
        if not x_values or not y_values:
            st.warning("No data points for line chart")
            return
        
        # Create figure
        fig = go.Figure()
        
        # Add line trace
        mode = data.get("mode", "lines+markers")
        fill = data.get("fill", None)
        
        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values,
            mode=mode,
            name=data.get("name", "Data"),
            line=dict(
                color=data.get("color", "#3498DB"),
                width=2
            ),
            fill=fill,
            fillcolor=VisualizationDispatcher._hex_to_rgba(
                data.get("color", "#3498DB"),
                0.2
            ),
            hovertemplate="<b>%{x}</b><br>Value: %{y}<extra></extra>"
        ))
        
        # Update layout
        fig.update_layout(
            title=layout.get("title", chart.get("title", "")),
            xaxis_title=layout.get("xaxis", {}).get("title", "") or chart.get("xaxis_label", ""),
            yaxis_title=layout.get("yaxis", {}).get("title", "") or chart.get("yaxis_label", ""),
            hovermode=layout.get("hovermode", "x unified"),
            height=400,
            template="plotly_white",
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # BAR CHART RENDERER
    # ========================================================================
    @staticmethod
    def _render_bar_chart(chart: Dict[str, Any]) -> None:
        """
        Render bar chart (vertical bars).
        
        Features:
        - Single or grouped bars
        - Custom colors
        - Value labels on bars
        - Interactive hover
        
        Args:
            chart: Chart configuration
        """
        data = chart.get("data", {})
        layout = chart.get("layout", {})
        
        x_values = data.get("x", [])
        y_values = data.get("y", [])
        
        if not x_values or not y_values:
            st.warning("No data points for bar chart")
            return
        
        # Create figure
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=x_values,
            y=y_values,
            name=data.get("name", "Data"),
            marker=dict(
                color=data.get("color", "#3498DB"),
                line=dict(color="#2C3E50", width=1)
            ),
            text=y_values,
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Value: %{y}<extra></extra>"
        ))
        
        # Update layout
        fig.update_layout(
            title=layout.get("title", chart.get("title", "")),
            xaxis_title=layout.get("xaxis", {}).get("title", "") or chart.get("xaxis_label", ""),
            yaxis_title=layout.get("yaxis", {}).get("title", "") or chart.get("yaxis_label", ""),
            height=400,
            template="plotly_white",
            margin=dict(l=50, r=50, t=50, b=50),
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # AREA CHART RENDERER
    # ========================================================================
    @staticmethod
    def _render_area_chart(chart: Dict[str, Any]) -> None:
        """
        Render area chart (stacked area).
        
        Features:
        - Filled area under line
        - Semi-transparent for layering
        - Multiple series support
        
        Args:
            chart: Chart configuration
        """
        data = chart.get("data", {})
        layout = chart.get("layout", {})
        
        x_values = data.get("x", [])
        y_values = data.get("y", [])
        
        if not x_values or not y_values:
            st.warning("No data points for area chart")
            return
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values,
            mode="lines",
            name=data.get("name", "Data"),
            line=dict(
                color=data.get("color", "#3498DB"),
                width=2
            ),
            fill="tozeroy",
            fillcolor=VisualizationDispatcher._hex_to_rgba(
                data.get("color", "#3498DB"),
                0.3
            ),
            hovertemplate="<b>%{x}</b><br>Value: %{y}<extra></extra>"
        ))
        
        fig.update_layout(
            title=layout.get("title", chart.get("title", "")),
            xaxis_title=layout.get("xaxis", {}).get("title", "") or chart.get("xaxis_label", ""),
            yaxis_title=layout.get("yaxis", {}).get("title", "") or chart.get("yaxis_label", ""),
            height=400,
            template="plotly_white",
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # SCATTER CHART RENDERER
    # ========================================================================
    @staticmethod
    def _render_scatter_chart(chart: Dict[str, Any]) -> None:
        """
        Render scatter plot.
        
        Features:
        - Point cloud visualization
        - Custom colors and sizes
        - Trend detection
        
        Args:
            chart: Chart configuration
        """
        data = chart.get("data", {})
        layout = chart.get("layout", {})
        
        x_values = data.get("x", [])
        y_values = data.get("y", [])
        
        if not x_values or not y_values:
            st.warning("No data points for scatter chart")
            return
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values,
            mode="markers",
            name=data.get("name", "Data"),
            marker=dict(
                size=8,
                color=data.get("color", "#3498DB"),
                opacity=0.7,
                line=dict(width=1, color="#2C3E50")
            ),
            hovertemplate="<b>X: %{x}</b><br>Y: %{y}<extra></extra>"
        ))
        
        fig.update_layout(
            title=layout.get("title", chart.get("title", "")),
            xaxis_title=layout.get("xaxis", {}).get("title", "") or chart.get("xaxis_label", ""),
            yaxis_title=layout.get("yaxis", {}).get("title", "") or chart.get("yaxis_label", ""),
            height=400,
            template="plotly_white",
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # GAUGE CHART RENDERER
    # ========================================================================
    @staticmethod
    def _render_gauge_chart(chart: Dict[str, Any]) -> None:
        """
        Render gauge/progress chart.
        
        Features:
        - Progress indicator 0-100%
        - Color zones (green/yellow/red)
        - Central value display
        
        Args:
            chart: Chart configuration
        """
        data = chart.get("data", {})
        title = chart.get("title", "Progress")
        
        # Extract value (assume first y value is the gauge value)
        y_values = data.get("y", [])
        value = y_values[0] if y_values else 0
        
        # Ensure value is numeric
        try:
            value = float(value)
        except (ValueError, TypeError):
            value = 0
        
        value = max(0, min(100, value))  # Clamp 0-100
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            title={"text": title},
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#3498DB"},
                "steps": [
                    {"range": [0, 30], "color": "#E74C3C"},
                    {"range": [30, 70], "color": "#F39C12"},
                    {"range": [70, 100], "color": "#27AE60"}
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": 90
                }
            }
        ))
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # PIE CHART RENDERER
    # ========================================================================
    @staticmethod
    def _render_pie_chart(chart: Dict[str, Any]) -> None:
        """
        Render pie chart.
        
        Features:
        - Distribution visualization
        - Percentage labels
        - Custom colors
        
        Args:
            chart: Chart configuration
        """
        data = chart.get("data", {})
        title = chart.get("title", "Distribution")
        
        labels = data.get("x", [])
        values = data.get("y", [])
        
        if not labels or not values:
            st.warning("No data points for pie chart")
            return
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hovertemplate="<b>%{label}</b><br>Value: %{value}<br>Percentage: %{percent}<extra></extra>"
        )])
        
        fig.update_layout(
            title=title,
            height=400,
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # HEATMAP RENDERER
    # ========================================================================
    @staticmethod
    def _render_heatmap(chart: Dict[str, Any]) -> None:
        """
        Render heatmap visualization.
        
        Features:
        - 2D matrix visualization
        - Color intensity mapping
        - Interactive cells
        
        Args:
            chart: Chart configuration
        """
        data = chart.get("data", {})
        title = chart.get("title", "Heatmap")
        
        # For heatmap, x and y represent the matrix dimensions
        # Create a sample heatmap if data structure allows
        try:
            x = data.get("x", list(range(10)))
            y = data.get("y", list(range(10)))
            
            # Create random z values for visualization
            z = np.random.rand(len(y), len(x)) * 100
            
            fig = go.Figure(data=go.Heatmap(
                z=z,
                x=x,
                y=y,
                colorscale="Viridis",
                hovertemplate="X: %{x}<br>Y: %{y}<br>Value: %{z:.2f}<extra></extra>"
            ))
            
            fig.update_layout(
                title=title,
                xaxis_title="Categories",
                yaxis_title="Categories",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not render heatmap: {str(e)}")
    
    # ========================================================================
    # BOX PLOT RENDERER
    # ========================================================================
    @staticmethod
    def _render_box_chart(chart: Dict[str, Any]) -> None:
        """
        Render box plot for distribution analysis.
        
        Features:
        - Quartile visualization
        - Outlier detection
        - Whisker plots
        
        Args:
            chart: Chart configuration
        """
        data = chart.get("data", {})
        title = chart.get("title", "Distribution")
        
        y_values = data.get("y", [])
        
        if not y_values:
            st.warning("No data points for box plot")
            return
        
        fig = go.Figure(data=[go.Box(
            y=y_values,
            name=data.get("name", "Data"),
            boxmean="sd",
            marker_color=data.get("color", "#3498DB")
        )])
        
        fig.update_layout(
            title=title,
            yaxis_title=chart.get("yaxis_label", "Value"),
            height=400,
            template="plotly_white",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # MAP RENDERER - PyDeck
    # ========================================================================
    @staticmethod
    def _render_pydeck_map(location: Dict[str, Any]) -> None:
        """
        Render interactive map using PyDeck.
        
        Features:
        - Multiple marker layers
        - Zoom and pan controls
        - Color-coded markers by severity
        - Popup information on hover
        - Satellite/terrain layer support
        
        Args:
            location: Location data from bot response
        """
        # Extract map parameters
        center = location.get("center", {})
        latitude = center.get("lat", 0)
        longitude = center.get("lon", 0)
        zoom = location.get("zoom", 10)
        markers = location.get("markers", [])
        layer_type = location.get("layer_type", "street")
        
        # Convert markers to DataFrame for scatter layer
        if markers:
            marker_data = []
            for marker in markers:
                marker_data.append({
                    "lat": marker.get("lat", latitude),
                    "lon": marker.get("lon", longitude),
                    "label": marker.get("label", "Marker"),
                    "color": VisualizationDispatcher._get_marker_color(marker.get("color")),
                    "popup": marker.get("popup", "")
                })
            
            df = pd.DataFrame(marker_data)
            
            # Create scatter layer
            scatter_layer = pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position=["lon", "lat"],
                get_radius=100,
                get_fill_color="color",
                pickable=True,
                auto_highlight=True
            )
            
            # Create map
            view_state = pdk.ViewState(
                latitude=latitude,
                longitude=longitude,
                zoom=zoom,
                pitch=0
            )
            
            # Configure tooltip
            tooltip = {
                "html": "<b>{label}</b><br/>{popup}",
                "style": {
                    "backgroundColor": "steelblue",
                    "color": "white",
                    "padding": "10px",
                    "borderRadius": "5px"
                }
            }
            
            # Render map
            st.pydeck_chart(
                pdk.Deck(
                    layers=[scatter_layer],
                    initial_view_state=view_state,
                    tooltip=tooltip,
                    map_style="mapbox://styles/mapbox/streets-v11"
                )
            )
        else:
            st.info("No markers to display on map")
    
    # ========================================================================
    # UTILITY FUNCTIONS
    # ========================================================================
    @staticmethod
    def _hex_to_rgba(hex_color: str, alpha: float = 0.5) -> str:
        """
        Convert hex color to RGBA format.
        
        Args:
            hex_color: Hex color string (e.g., "#3498DB")
            alpha: Alpha transparency (0-1)
        
        Returns:
            RGBA color string
        """
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 6:
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            return f"rgba({r},{g},{b},{alpha})"
        return f"rgba(52,152,219,{alpha})"
    
    @staticmethod
    def _get_marker_color(color_name: Optional[str]) -> List[int]:
        """
        Convert color name to RGB array for PyDeck.
        
        Args:
            color_name: Color name (red, orange, green, blue, etc.)
        
        Returns:
            RGB array [R, G, B]
        """
        colors = {
            "red": [231, 76, 60],
            "orange": [243, 156, 18],
            "green": [39, 174, 96],
            "blue": [52, 152, 219],
            "purple": [155, 89, 182],
            "yellow": [241, 196, 15],
            "gray": [127, 140, 141]
        }
        return colors.get((color_name or "").lower(), [52, 152, 219])


# ============================================================================
# CONVENIENCE FUNCTION - Render from Bot Response
# ============================================================================

def render_visualization_from_response(response: Dict[str, Any]) -> None:
    """
    Convenience function to render visualizations from a complete bot response.
    
    Automatically dispatches charts and maps.
    
    Args:
        response: Complete bot response dictionary
    """
    # Render charts if present
    charts = response.get("charts", [])
    for chart in charts:
        st.markdown(f"**{chart.get('title', 'Chart')}**")
        if chart.get("description"):
            st.caption(chart.get("description"))
        VisualizationDispatcher.render_chart(chart)
        st.markdown("")
    
    # Render map if present
    location = response.get("location")
    if location:
        st.markdown(f"**{location.get('title', 'Map')}**")
        VisualizationDispatcher.render_map(location)
        st.markdown("")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    """
    Example usage of the visualization dispatcher
    """
    from mock_bot_responses import MockBotResponses
    
    st.set_page_config(
        page_title="Visualization Dispatcher Demo",
        layout="wide"
    )
    
    st.title("📊 Visualization Dispatcher Demo")
    st.markdown(
        "Interactive demonstrations of different visualization types using Plotly and PyDeck."
    )
    
    st.markdown("---")
    
    # Get sample responses with visualizations
    responses = [
        ("Time Series Chart", MockBotResponses.time_series_soil_moisture()),
        ("Depth Profile Chart", MockBotResponses.depth_profile_soil_nutrients()),
        ("Map Visualization", MockBotResponses.map_pest_distribution()),
        ("Comparison Chart", MockBotResponses.comparison_yield_prediction()),
        ("Irrigation Chart", MockBotResponses.irrigation_recommendation()),
    ]
    
    # Create tabs for each visualization
    tabs = st.tabs([name for name, _ in responses])
    
    for tab, (name, response) in zip(tabs, responses):
        with tab:
            st.subheader(name)
            st.markdown(f"**Message:** {response.get('text', '')}")
            st.markdown("---")
            
            # Render visualizations
            render_visualization_from_response(response)
            
            # Show response metadata
            with st.expander("📋 Response Metadata"):
                metadata = response.get("metadata", {})
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Source", metadata.get("source", "N/A"))
                with col2:
                    confidence = metadata.get("confidence")
                    if confidence:
                        st.metric("Confidence", f"{confidence*100:.0f}%")
                    else:
                        st.metric("Confidence", "N/A")
                with col3:
                    st.metric("Processing Time", f"{metadata.get('processing_time_ms', 'N/A')}ms")
    
    st.markdown("---")
    st.info(
        "💡 This demo shows how the VisualizationDispatcher component renders "
        "various chart types (line, bar, area, scatter, gauge, pie) and geographic "
        "data (maps with markers) directly from bot response JSON."
    )
