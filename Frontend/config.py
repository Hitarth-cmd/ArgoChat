"""
Configuration and Constants
Centralized settings for the AgroChat application
"""

# ============================================================================
# UI CONFIGURATION
# ============================================================================

APP_TITLE = "🌾 AgroChat - Your AI Farming Assistant"
APP_DESCRIPTION = "Get instant insights on crop health, weather, soil, pests, and more."
APP_ICON = "🌾"

# Page layout
LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"

# ============================================================================
# COLORS & STYLING
# ============================================================================

THEME_COLORS = {
    "primary": "#2d5016",      # Dark green
    "secondary": "#4caf50",    # Green
    "accent": "#ff7f0e",       # Orange
    "error": "#d62728",        # Red
    "warning": "#ff7f0e",      # Orange
    "success": "#2ca02c",      # Green
    "info": "#1f77b4",         # Blue
}

INSIGHT_COLOR_MAP = {
    "green": "#1f77b4",
    "red": "#d62728",
    "orange": "#ff7f0e",
    "blue": "#1f77b4",
}

# ============================================================================
# CHART CONFIGURATION
# ============================================================================

CHART_HEIGHT = 300
CHART_TEMPLATE = "plotly_white"
CHART_HOVERMODE = "x unified"

# Supported chart types
SUPPORTED_CHART_TYPES = [
    "line",
    "bar",
    "area",
    "scatter",
    "gauge",
    "map"
]

# ============================================================================
# RESPONSE TYPES
# ============================================================================

RESPONSE_TYPES = {
    "TEXT": "text",
    "CHART": "chart",
    "INSIGHTS": "insights",
    "RECOMMENDATION": "recommendation",
    "ALERT": "alert",
}

ALERT_TYPES = {
    "ERROR": "error",
    "WARNING": "warning",
    "SUCCESS": "success",
    "INFO": "info",
}

TREND_TYPES = {
    "UP": "up",
    "DOWN": "down",
    "STABLE": "stable",
}

# ============================================================================
# QUICK COMMANDS MAPPING
# ============================================================================

QUICK_COMMANDS = {
    "Crop Health": "How's my crop health today?",
    "Weather": "What's the weather forecast?",
    "Soil Analysis": "Analyze my soil conditions",
    "Pest Alert": "Any pest alerts in my area?",
    "Market Prices": "What are the current market prices?",
    "Recommendations": "What should I plant next season?",
    "Equipment": "Check equipment maintenance status",
}

# ============================================================================
# KEYWORD TO RESPONSE MAPPING
# ============================================================================

KEYWORD_RESPONSE_MAP = {
    "crop health": "crop_health",
    "health": "crop_health",
    "weather": "weather",
    "forecast": "weather",
    "soil": "soil",
    "pest": "pest",
    "market": "market",
    "price": "market",
    "recommend": "recommendation",
    "plant": "recommendation",
    "equipment": "maintenance",
    "maintenance": "maintenance",
}

# Default response when no keyword matches
DEFAULT_RESPONSE = "crop_health"

# ============================================================================
# CHAT SETTINGS
# ============================================================================

MAX_HISTORY_DISPLAY = 100  # Maximum messages to show in chat
CHAT_INPUT_PLACEHOLDER = "Ask me about your farm... (Try: 'Crop health', 'Weather', 'Soil analysis')"

# User & Bot avatars
USER_AVATAR = "👨‍🌾"
BOT_AVATAR = "🤖"

# ============================================================================
# SIDEBAR CONTENT
# ============================================================================

SIDEBAR_TITLE = "💬 Quick Commands"
SIDEBAR_ABOUT = """
**AgroChat** - Your AI farming assistant

- 🌾 Crop health monitoring
- 🌤️ Weather forecasts
- 🧪 Soil analysis
- 🚨 Pest alerts
- 💹 Market insights
- 🤖 AI recommendations

*Built with Streamlit & structured JSON responses*
"""

FOOTER_TEXT = """
<div style='text-align: center; color: #666; font-size: 12px;'>

**AgroChat** is a demonstration of a structured JSON-based chatbot frontend.

✨ Built with Streamlit | Plotly | PyDeck

🔒 All data is mock/demo data. This is a frontend-only prototype with no backend API calls.

</div>
"""

# ============================================================================
# MOCK DATA SETTINGS
# ============================================================================

# Enable/disable mock responses
USE_MOCK_RESPONSES = True

# Mock response delay (in seconds) - can simulate API latency
MOCK_RESPONSE_DELAY = 0  # Set to > 0 to add simulated delay

# ============================================================================
# LOGGING & DEBUGGING
# ============================================================================

# Show debug info
DEBUG_MODE = False

# Log all chat messages
LOG_MESSAGES = False

# Show raw JSON by default
SHOW_JSON_BY_DEFAULT = False

# ============================================================================
# ADVANCED SETTINGS
# ============================================================================

# Session state keys
SESSION_KEYS = {
    "chat_history": "chat_history",
    "user_input": "current_user_input",
    "demo_responses": "demo_responses",
    "quick_command": "quick_command",
    "show_json": "show_json",
}

# Message metadata
MESSAGE_METADATA = {
    "track_timestamps": True,
    "track_response_types": True,
    "track_performance": False,
}

# ============================================================================
# VALIDATION
# ============================================================================

# Minimum/maximum constraints
MIN_MESSAGE_LENGTH = 1
MAX_MESSAGE_LENGTH = 1000
MIN_INSIGHT_VALUE_LENGTH = 1
MAX_INSIGHTS_PER_RESPONSE = 12
MAX_CHARTS_PER_RESPONSE = 4
MAX_RECOMMENDATIONS_PER_RESPONSE = 10

# ============================================================================
# API ENDPOINTS (for future backend integration)
# ============================================================================

# API Configuration (when backend is added)
API_CONFIG = {
    "base_url": "https://api.agrochat.example.com",
    "timeout": 10,  # seconds
    "retry_attempts": 3,
    "endpoints": {
        "analyze": "/api/analyze",
        "forecast": "/api/forecast",
        "recommendations": "/api/recommendations",
        "alerts": "/api/alerts",
    }
}

# ============================================================================
# FEATURE FLAGS
# ============================================================================

FEATURES = {
    "enable_chat_history": True,
    "enable_quick_commands": True,
    "enable_raw_json_view": True,
    "enable_clear_history": True,
    "enable_charts": True,
    "enable_insights": True,
    "enable_recommendations": True,
    "enable_alerts": True,
    "enable_export": False,  # Future feature
    "enable_voice_input": False,  # Future feature
    "enable_file_upload": False,  # Future feature
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_response_type_display(response_type: str) -> str:
    """Get human-readable response type"""
    type_display = {
        "text": "💬 Text",
        "chart": "📊 Chart",
        "insights": "📈 Insights",
        "recommendation": "💡 Recommendation",
        "alert": "🚨 Alert",
    }
    return type_display.get(response_type, response_type)


def get_alert_emoji(alert_type: str) -> str:
    """Get emoji for alert type"""
    emoji_map = {
        "error": "❌",
        "warning": "⚠️",
        "success": "✅",
        "info": "ℹ️",
    }
    return emoji_map.get(alert_type, "📢")


def get_trend_emoji(trend: str) -> str:
    """Get emoji for trend indicator"""
    trend_map = {
        "up": "📈",
        "down": "📉",
        "stable": "➡️",
    }
    return trend_map.get(trend, "")


def sanitize_user_input(text: str) -> str:
    """Sanitize and validate user input"""
    text = text.strip()
    if len(text) < MIN_MESSAGE_LENGTH or len(text) > MAX_MESSAGE_LENGTH:
        return ""
    return text


# ============================================================================
# CSS STYLING
# ============================================================================

CUSTOM_CSS = """
    <style>
    .main {
        padding-top: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    h1 {
        color: #2d5016;
        border-bottom: 3px solid #4caf50;
        padding-bottom: 0.5rem;
    }
    h3 {
        color: #2d5016;
    }
    .insight-card {
        border-left: 5px solid #1f77b4;
        padding: 15px;
        background-color: rgba(31, 119, 180, 0.05);
        border-radius: 5px;
        margin-bottom: 10px;
    }
    </style>
    """
