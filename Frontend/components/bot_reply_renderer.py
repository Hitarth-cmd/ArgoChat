"""
Bot Reply Renderer Component
Renders structured bot responses to Streamlit UI following the AgroChat schema
Handles text, insights, metadata, and visualization placeholders
"""

from typing import Dict, Any, Optional
import streamlit as st
from datetime import datetime
from .visual_dispatcher import VisualizationDispatcher


class BotReplyRenderer:
    """
    Renders bot responses in Streamlit with clean layout and spacing.
    
    Supports all response types:
    - text: Simple text responses
    - chart: Time series and data visualizations
    - insights: Metric cards and KPIs
    - recommendation: Action items and suggestions
    - alert: Errors and warnings
    - composite: Multiple components combined
    """
    
    # Color palette for severity levels
    ALERT_COLORS = {
        "error": "🔴",
        "warning": "🟠",
        "info": "🔵",
        "success": "🟢"
    }
    
    TREND_ICONS = {
        "up": "📈",
        "down": "📉",
        "stable": "➡️"
    }
    
    COLOR_BADGES = {
        "green": "✅",
        "red": "❌",
        "yellow": "⚠️",
        "blue": "ℹ️",
        "orange": "⚡",
        "purple": "🎯"
    }
    
    @staticmethod
    def render(response: Dict[str, Any], container: Optional[Any] = None) -> None:
        """
        Main render function - orchestrates all sub-components.
        
        Args:
            response: Bot response dictionary following schema
            container: Optional Streamlit container (e.g., st.container())
                      If None, renders to main page
        """
        # Use provided container or default to main page
        target = container if container else st
        
        if container:
            with container:
                # 1. RENDER TEXT CONTENT (always first if present)
                if response.get("text"):
                    BotReplyRenderer._render_text(response["text"])
                
                # 2. RENDER CONTENT BASED ON MESSAGE TYPE
                message_type = response.get("message_type", "text")
                
                if message_type == "text":
                    # Text-only: already rendered above
                    pass
                
                elif message_type == "chart":
                    # Charts and maps
                    BotReplyRenderer._render_charts_section(response)
                    if response.get("location"):
                        BotReplyRenderer._render_map_section(response["location"])
                
                elif message_type == "insights":
                    # Metric cards
                    BotReplyRenderer._render_insights_section(response.get("insights", []))
                
                elif message_type == "recommendation":
                    # Action items
                    BotReplyRenderer._render_recommendations_section(
                        response.get("recommendations", [])
                    )
                
                elif message_type == "alert":
                    # Errors and warnings
                    BotReplyRenderer._render_alert_section(response.get("alert", {}))
                
                elif message_type == "composite":
                    # Multiple components
                    if response.get("insights"):
                        BotReplyRenderer._render_insights_section(response["insights"])
                    
                    if response.get("charts"):
                        BotReplyRenderer._render_charts_section(response)
                    
                    if response.get("location"):
                        BotReplyRenderer._render_map_section(response["location"])
                    
                    if response.get("recommendations"):
                        BotReplyRenderer._render_recommendations_section(
                            response["recommendations"]
                        )
                
                # 3. RENDER RELATED LINKS (if any)
                if response.get("links"):
                    BotReplyRenderer._render_links_section(response["links"])
                
                # 4. RENDER METADATA FOOTER
                BotReplyRenderer._render_metadata_footer(response.get("metadata", {}))
        else:
            # 1. RENDER TEXT CONTENT (always first if present)
            if response.get("text"):
                BotReplyRenderer._render_text(response["text"])
            
            # 2. RENDER CONTENT BASED ON MESSAGE TYPE
            message_type = response.get("message_type", "text")
            
            if message_type == "text":
                # Text-only: already rendered above
                pass
            
            elif message_type == "chart":
                # Charts and maps
                BotReplyRenderer._render_charts_section(response)
                if response.get("location"):
                    BotReplyRenderer._render_map_section(response["location"])
            
            elif message_type == "insights":
                # Metric cards
                BotReplyRenderer._render_insights_section(response.get("insights", []))
            
            elif message_type == "recommendation":
                # Action items
                BotReplyRenderer._render_recommendations_section(
                    response.get("recommendations", [])
                )
            
            elif message_type == "alert":
                # Errors and warnings
                BotReplyRenderer._render_alert_section(response.get("alert", {}))
            
            elif message_type == "composite":
                # Multiple components
                if response.get("insights"):
                    BotReplyRenderer._render_insights_section(response["insights"])
                
                if response.get("charts"):
                    BotReplyRenderer._render_charts_section(response)
                
                if response.get("location"):
                    BotReplyRenderer._render_map_section(response["location"])
                
                if response.get("recommendations"):
                    BotReplyRenderer._render_recommendations_section(
                        response["recommendations"]
                    )
            
            # 3. RENDER RELATED LINKS (if any)
            if response.get("links"):
                BotReplyRenderer._render_links_section(response["links"])
            
            # 4. RENDER METADATA FOOTER
            BotReplyRenderer._render_metadata_footer(response.get("metadata", {}))
    
    
    # ========================================================================
    # TEXT RENDERING
    # ========================================================================
    @staticmethod
    def _render_text(text: str) -> None:
        """
        Render primary text content with premium spacing using the bot-bubble style.
        
        Args:
            text: Message text to display
        """
        now = datetime.now().strftime("%H:%M")
        
        html = f"""<div class='chat-message-bot'><div style='display: flex; flex-direction: column; align-items: flex-start; width: 100%;'><div class='bot-bubble'>{text.strip()}</div><div class='message-time bot-time'>{now}</div></div></div>"""
        st.markdown(html, unsafe_allow_html=True)
    
    # ========================================================================
    # INSIGHTS RENDERING - Metric Cards
    # ========================================================================
    @staticmethod
    def _render_insights_section(insights: list) -> None:
        """
        Render insights as a grid of metric cards with premium spacing.
        
        Layout: Multiple columns (2-4 per row depending on screen)
        Each card shows: label, value, unit, trend, color
        
        Args:
            insights: List of insight card dictionaries
        """
        st.markdown("### 📊 Key Metrics")
        st.markdown("")  # Premium spacing
        
        # Create columns based on number of insights
        num_insights = len(insights)
        cols_per_row = min(4, max(1, num_insights))
        
        for i in range(0, num_insights, cols_per_row):
            cols = st.columns(cols_per_row, gap="medium")
            
            for col_idx, col in enumerate(cols):
                if i + col_idx >= num_insights:
                    break
                
                insight = insights[i + col_idx]
                BotReplyRenderer._render_insight_card(insight, col)
        
        st.markdown("")  # Clean spacing after metrics
    
    @staticmethod
    def _render_insight_card(insight: Dict[str, Any], container: Any) -> None:
        """
        Render a single insight/metric card with premium design.
        
        Card displays:
        - Icon and label
        - Value in large text
        - Unit and trend indicator
        - Subtle elevation and borders
        
        Args:
            insight: Insight card dictionary
            container: Streamlit column container
        """
        with container:
            label = insight.get("label", "Unknown")
            value = insight.get("value", "—")
            unit = insight.get("unit")
            trend = insight.get("trend")
            color = insight.get("color", "blue")
            
            # Color mapping - Premium palette
            color_map = {
                "green": "#10B981",
                "red": "#EF4444",
                "orange": "#F97316",
                "blue": "#3B82F6",
                "yellow": "#FBBF24",
                "purple": "#A855F7",
            }
            accent_color = color_map.get(color, "#3B82F6")
            
            # Build trend indicator
            trend_text = ""
            if trend and trend in BotReplyRenderer.TREND_ICONS:
                trend_text = BotReplyRenderer.TREND_ICONS[trend]
            
            # Format unit
            unit_text = f" {unit}" if unit else ""
            
            # Premium card styling with subtle depth
            card_html = f"""
            <div style="
                border-left: 3px solid {accent_color};
                padding: 16px 18px;
                margin-bottom: 0px;
                background-color: rgba(30, 41, 59, 0.6);
                border-radius: 8px;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
                border: 1px solid rgba(71, 85, 105, 0.3);
                transition: box-shadow 0.2s ease;
            ">
                <div style="
                    font-size: 11px;
                    color: #94A3B8;
                    margin-bottom: 8px;
                    text-transform: uppercase;
                    letter-spacing: 0.4px;
                    font-weight: 500;
                ">
                    {label}
                </div>
                <div style="
                    font-size: 26px;
                    font-weight: 600;
                    color: {accent_color};
                    letter-spacing: -0.5px;
                    line-height: 1.1;
                    margin-bottom: 8px;
                ">
                    {value}<span style="font-size: 14px; font-weight: 500;">{unit_text}</span>
                </div>
                {f'<div style="font-size: 12px; color: {accent_color}; font-weight: 500;">{trend_text}</div>' if trend_text else ''}
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
    
    # ========================================================================
    # CHARTS RENDERING - Premium Visualization
    # ========================================================================
    @staticmethod
    def _render_charts_section(response: Dict[str, Any]) -> None:
        """
        Render charts section with premium styling and spacing.
        
        Renders:
        - Chart title
        - Interactive chart visualization using Plotly
        - Clean metadata layout
        
        Args:
            response: Bot response containing charts
        """
        charts = response.get("charts", [])
        
        if not charts:
            return
        
        st.markdown("### 📈 Data Visualization")
        st.markdown("")  # Premium spacing
        
        for idx, chart in enumerate(charts, 1):
            chart_type = chart.get("type", "unknown")
            title = chart.get("title", "Chart")
            description = chart.get("description", "")
            
            with st.container():
                # Chart title with premium typography
                st.markdown(f"**{title}**")
                if description:
                    st.markdown(f"<small>{description}</small>", unsafe_allow_html=True)
                
                # Render actual chart
                try:
                    VisualizationDispatcher.render_chart(chart)
                except Exception as e:
                    st.error(f"Error rendering chart: {str(e)}")
                
                st.markdown("")  # Clean spacing between charts
    
    # ========================================================================
    # MAP RENDERING - Premium Visualization
    # ========================================================================
    @staticmethod
    def _render_map_section(location: Dict[str, Any]) -> None:
        """
        Render map section with premium styling and spacing.
        
        Args:
            location: Location/map data dictionary
        """
        st.markdown("### 🗺️ Geographic Data")
        st.markdown("")  # Premium spacing
        
        title = location.get("title", "Location Map")
        st.markdown(f"**{title}**")
        
        # Map metadata
        center = location.get("center", {})
        zoom = location.get("zoom", 10)
        markers = location.get("markers", [])
        layer_type = location.get("layer_type", "street")
        
        # Render actual map if available
        try:
            VisualizationDispatcher.render_map(location)
        except Exception:
            st.info(f"🗺️ Map visualization not yet available")
        
        # Display marker summary
        if markers:
            st.markdown("**Marker Locations:**")
            marker_cols = st.columns(min(3, len(markers)))
            
            for idx, marker in enumerate(markers[:6]):  # Show first 6
                col = marker_cols[idx % len(marker_cols)]
                with col:
                    label = marker.get("label", "Marker")
                    color = marker.get("color", "gray")
                    popup = marker.get("popup", "")
                    
                    color_emoji = {
                        "red": "🔴",
                        "orange": "🟠",
                        "green": "🟢",
                        "blue": "🔵",
                        "purple": "🟣"
                    }.get(color, "⭕")
                    
                    st.markdown(f"{color_emoji} **{label}**")
                    if popup:
                        st.markdown(f"<small>{popup[:60] + '...' if len(popup) > 60 else popup}</small>", unsafe_allow_html=True)
        
        st.markdown("")  # Premium spacing
    
    # ========================================================================
    # RECOMMENDATIONS RENDERING - Premium List
    # ========================================================================
    @staticmethod
    def _render_recommendations_section(recommendations: list) -> None:
        """
        Render recommendations as clean action items with premium spacing.
        
        Layout: Numbered list with clean typography
        Each item is an actionable recommendation
        
        Args:
            recommendations: List of recommendation strings
        """
        if not recommendations:
            return
        
        st.markdown("### 💡 Recommendations")
        st.markdown("")  # Premium spacing
        
        for idx, recommendation in enumerate(recommendations, 1):
            # Premium list item styling
            st.markdown(f"**{idx}.** {recommendation}")
        
        st.markdown("")  # Premium spacing
    
    # ========================================================================
    # ALERT RENDERING - Premium Alerts
    # ========================================================================
    @staticmethod
    def _render_alert_section(alert: Dict[str, Any]) -> None:
        """
        Render alert/error message with premium styling and spacing.
        
        Severity types:
        - error: Red, critical attention needed
        - warning: Orange, caution required
        - info: Blue, informational
        - success: Green, positive outcome
        
        Args:
            alert: Alert dictionary with type, title, message, etc.
        """
        if not alert:
            return
        
        alert_type = alert.get("type", "info")
        title = alert.get("title", "Alert")
        message = alert.get("message", "")
        code = alert.get("code")
        details = alert.get("details")
        action = alert.get("action")
        
        # Determine Streamlit alert function
        if alert_type == "error":
            alert_func = st.error
            icon = "🔴"
        elif alert_type == "warning":
            alert_func = st.warning
            icon = "🟠"
        elif alert_type == "success":
            alert_func = st.success
            icon = "🟢"
        else:  # info
            alert_func = st.info
            icon = "🔵"
        
        # Render alert with clean formatting
        alert_message = f"**{icon} {title}**\n\n{message}"
        
        if code:
            alert_message += f"\n\n**Error Code:** `{code}`"
        
        alert_func(alert_message)
        
        # Details in expandable section
        if details:
            with st.expander("📋 Technical Details"):
                st.code(details, language="text")
        
        # Action recommendation
        if action:
            st.info(f"**💡 Suggested Action:**\n\n{action}")
        
        st.markdown("")  # Premium spacing
    
    # ========================================================================
    # LINKS RENDERING
    # ========================================================================
    @staticmethod
    def _render_links_section(links: list) -> None:
        """
        Render related links and resources.
        
        Layout: Grid of link buttons/cards
        Types: documentation, related_query, support, external
        
        Args:
            links: List of link dictionaries
        """
        if not links:
            return
        
        st.subheader("🔗 Related Resources")
        
        cols = st.columns(min(3, len(links)))
        
        for idx, link in enumerate(links):
            col = cols[idx % len(cols)]
            with col:
                text = link.get("text", "Link")
                url = link.get("url", "#")
                link_type = link.get("type", "external")
                
                # Icon for link type
                type_icons = {
                    "documentation": "📖",
                    "related_query": "🔍",
                    "support": "💬",
                    "external": "🔗"
                }
                icon = type_icons.get(link_type, "🔗")
                
                # Render as markdown link
                st.markdown(f"[{icon} {text}]({url})")
        
        st.markdown("")  # Spacing
    
    # ========================================================================
    # METADATA FOOTER
    # ========================================================================
    @staticmethod
    def _render_metadata_footer(metadata: Dict[str, Any]) -> None:
        """
        Render metadata in a subtle footer.
        
        Shows:
        - Source (ai_model, database, api, etc.)
        - Confidence level with progress bar
        - Model version
        - Processing time
        - Data freshness
        
        Args:
            metadata: Metadata dictionary from response
        """
        if not metadata:
            return
        
        with st.container():
            st.markdown("---")
            
            # Create metadata columns
            col1, col2, col3, col4, col5 = st.columns(5)
            
            # Source
            source = metadata.get("source", "unknown")
            with col1:
                st.caption(f"📡 **Source:** {source}")
            
            # Confidence with progress bar
            confidence = metadata.get("confidence")
            with col2:
                if confidence is not None:
                    st.caption(f"✓ **Confidence:** {confidence*100:.0f}%")
                    st.progress(confidence)
                else:
                    st.caption("✓ **Confidence:** N/A")
            
            # Model version
            model_version = metadata.get("model_version")
            with col3:
                if model_version:
                    st.caption(f"⚙️ **Model:** {model_version}")
                else:
                    st.caption("⚙️ **Model:** N/A")
            
            # Processing time
            processing_time = metadata.get("processing_time_ms")
            with col4:
                if processing_time:
                    st.caption(f"⏱️ **Time:** {processing_time}ms")
                else:
                    st.caption("⏱️ **Time:** N/A")
            
            # Data freshness
            freshness = metadata.get("data_freshness")
            with col5:
                if freshness:
                    st.caption(f"🕐 **Fresh:** {freshness}")
                else:
                    st.caption("🕐 **Fresh:** N/A")


# ============================================================================
# HELPER FUNCTION - Render with Custom Styling
# ============================================================================

def render_bot_message(response: Dict[str, Any], key: Optional[str] = None) -> None:
    """
    Convenience function to render a bot message with default styling.
    
    This wraps BotReplyRenderer.render() with additional styling.
    
    Args:
        response: Bot response dictionary
        key: Optional Streamlit key for reproducibility
    """
    # Optional: Add custom CSS styling here
    st.markdown(
        """
        <style>
        .bot-message {
            background-color: #F8F9FA;
            border-left: 4px solid #3498DB;
            padding: 12px;
            margin: 8px 0;
            border-radius: 4px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Render the response
    with st.container():
        BotReplyRenderer.render(response)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    """
    Example usage of the bot reply renderer
    """
    from mock_bot_responses import MockBotResponses
    
    st.set_page_config(
        page_title="Bot Reply Renderer Demo",
        layout="wide"
    )
    
    st.title("🤖 Bot Reply Renderer Demo")
    st.markdown(
        "This page demonstrates the BotReplyRenderer component with various response types."
    )
    
    st.markdown("---")
    
    # Get all mock responses
    responses = [
        ("Time Series", MockBotResponses.time_series_soil_moisture()),
        ("Depth Profile", MockBotResponses.depth_profile_soil_nutrients()),
        ("Map Analysis", MockBotResponses.map_pest_distribution()),
        ("Comparison", MockBotResponses.comparison_yield_prediction()),
        ("Error Alert", MockBotResponses.error_weather_service_down()),
        ("Irrigation", MockBotResponses.irrigation_recommendation()),
    ]
    
    # Render each response in a tab
    tabs = st.tabs([name for name, _ in responses])
    
    for tab, (name, response) in zip(tabs, responses):
        with tab:
            st.subheader(f"Response: {name}")
            st.markdown(f"**Type:** {response['message_type']}")
            
            st.markdown("---")
            
            # Render the response
            BotReplyRenderer.render(response)
            
            st.markdown("---")
            
            # Show raw JSON for debugging
            with st.expander("📋 Raw JSON Response"):
                import json
                st.json(response)
