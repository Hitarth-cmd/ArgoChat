# 🛠️ Development & Extension Guide

## How to Extend AgroChat

This guide shows you how to add new features, response types, and visualizations.

---

## 📝 Adding a New Mock Response

Let's say you want to add a "Water Management" response.

### Step 1: Define in schemas.py

No changes needed - the generic `BotResponse` handles all types!

### Step 2: Create in mock_responses.py

```python
@staticmethod
def water_management() -> BotResponse:
    """Water management and irrigation recommendations"""
    return BotResponse(
        message_id=get_uuid(),
        timestamp=get_timestamp(),
        message_type=ResponseType.INSIGHTS.value,
        text="💧 Water Management Report - Your field",
        insights=[
            InsightCard(
                label="Current Moisture",
                value="65",
                unit="%",
                trend="down",
                color="blue"
            ),
            InsightCard(
                label="Irrigation Needed",
                value="Yes",
                unit="",
                trend="down",
                color="orange"
            ),
            InsightCard(
                label="Water Stress Level",
                value="Moderate",
                unit="",
                color="orange"
            ),
            InsightCard(
                label="Recommended Irrigation",
                value="25",
                unit="mm",
                color="blue"
            ),
        ],
        charts=[
            ChartData(
                type=ChartType.LINE.value,
                title="Soil Moisture Over Time",
                data={
                    "x": ["Mon", "Tue", "Wed", "Thu", "Fri"],
                    "y": [55, 58, 62, 65, 63],
                    "name": "Moisture %"
                }
            ),
        ],
        recommendations=[
            "Irrigate today - moisture is dropping",
            "Plan for 25mm of water",
            "Irrigate in early morning (5-7 AM)",
            "Use drip irrigation for better efficiency",
            "Monitor weather for rain (may reduce need)"
        ],
        metadata={
            "sensor_coverage": "100%",
            "last_update": "2025-01-09 15:00 UTC",
            "confidence": 0.96
        }
    )
```

### Step 3: Add Rendering (optional - already generic)

The `ResponseRenderer` automatically handles all response types!

### Step 4: Wire into app.py

Add to the `response_map` in `app.py`:

```python
response_map = {
    "water": MockBotResponses.water_management,
    "irrigation": MockBotResponses.water_management,
    "moisture": MockBotResponses.water_management,
    # ... existing mappings ...
}
```

Also add to `QUICK_COMMANDS` in `config.py`:

```python
QUICK_COMMANDS = {
    "Water Management": "How's my water situation?",
    # ... existing commands ...
}
```

### Done! ✅

Now typing "water", "irrigation", or "moisture" will trigger your new response!

---

## 🎨 Adding a New Chart Type

Let's add a **Heatmap** chart type.

### Step 1: Update schemas.py

```python
class ChartType(Enum):
    """Supported chart types"""
    LINE = "line"
    BAR = "bar"
    AREA = "area"
    SCATTER = "scatter"
    GAUGE = "gauge"
    MAP = "map"
    HEATMAP = "heatmap"  # NEW!
```

### Step 2: Create Rendering Function in components.py

```python
def render_heatmap(data: dict, title: str) -> None:
    """Render heatmap using Plotly"""
    import plotly.graph_objects as go
    
    fig = go.Figure(data=go.Heatmap(
        z=data.get("z", []),
        x=data.get("x", []),
        y=data.get("y", []),
        colorscale="Viridis"
    ))
    
    fig.update_layout(
        title=title,
        height=300,
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)
```

### Step 3: Add to Rendering Switch in components.py

```python
@staticmethod
def render_single_chart(chart: ChartData) -> None:
    """Render a single chart based on type"""
    if chart.type == "line":
        render_line_chart(chart.data, chart.title)
    elif chart.type == "bar":
        render_bar_chart(chart.data, chart.title)
    # ... other types ...
    elif chart.type == "heatmap":  # NEW!
        render_heatmap(chart.data, chart.title)
    else:
        st.warning(f"Chart type '{chart.type}' not yet supported")
```

### Step 4: Use in a Response

```python
ChartData(
    type=ChartType.HEATMAP.value,
    title="Soil Nutrient Distribution",
    data={
        "x": ["Zone A", "Zone B", "Zone C"],
        "y": ["0-10cm", "10-20cm", "20-30cm"],
        "z": [[45, 42, 40], [38, 35, 32], [28, 25, 22]]
    }
)
```

### Done! ✅

Heatmaps now render automatically in any response!

---

## 🎯 Adding a New Insight Color

Let's add a **Purple** color for insights.

### Step 1: Update config.py

```python
INSIGHT_COLOR_MAP = {
    "green": "#2ca02c",
    "red": "#d62728",
    "orange": "#ff7f0e",
    "blue": "#1f77b4",
    "purple": "#9467bd",  # NEW!
}
```

### Step 2: Use in InsightCard

```python
InsightCard(
    label="Risk Assessment",
    value="Medium",
    color="purple"
)
```

### Done! ✅

The card automatically renders with the purple color!

---

## 🔗 Connecting a Real Backend API

### Current: Mock Responses
```
User Input → Keyword Match → Mock Function → BotResponse → Render
```

### Target: Real API
```
User Input → API Call → Parse JSON → BotResponse → Render
```

### Implementation

**Step 1: Create API Client (api_client.py)**

```python
"""API Client for Backend Integration"""
import requests
from schemas import BotResponse
from typing import Optional
import json

class BotAPIClient:
    """Client for communicating with bot backend"""
    
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
    
    def analyze_farm(self, query: str, field_id: Optional[str] = None) -> BotResponse:
        """Send query to backend and get structured response"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/analyze",
                json={
                    "query": query,
                    "field_id": field_id,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=self.timeout
            )
            response.raise_for_status()
            
            # Parse JSON response into BotResponse
            data = response.json()
            
            # Reconstruct nested objects
            insights = None
            if data.get("insights"):
                from schemas import InsightCard
                insights = [InsightCard(**i) for i in data["insights"]]
            
            charts = None
            if data.get("charts"):
                from schemas import ChartData
                charts = [ChartData(**c) for c in data["charts"]]
            
            return BotResponse(
                message_id=data.get("message_id", ""),
                timestamp=data.get("timestamp", ""),
                message_type=data.get("message_type", "text"),
                text=data.get("text"),
                insights=insights,
                charts=charts,
                recommendations=data.get("recommendations"),
                alert=data.get("alert"),
                metadata=data.get("metadata")
            )
        
        except requests.RequestException as e:
            # Fallback to mock response on API error
            st.error(f"Backend API error: {str(e)}")
            from mock_responses import MockBotResponses
            return MockBotResponses.crop_health_analysis()
        
        except json.JSONDecodeError:
            st.error("Invalid response from backend API")
            from mock_responses import MockBotResponses
            return MockBotResponses.crop_health_analysis()
    
    def close(self):
        """Close API session"""
        self.session.close()
```

**Step 2: Update app.py**

```python
# At the top of app.py
from api_client import BotAPIClient

# Initialize API client
API_URL = "https://your-backend.com"  # or from environment variable
bot_api = BotAPIClient(API_URL)

# In the message processing section, replace:
# bot_response = MockBotResponses.crop_health_analysis()
# With:
bot_response = bot_api.analyze_farm(user_input, field_id=None)
```

**Step 3: Add Error Handling**

```python
# Wrap in try-except for graceful degradation
try:
    bot_response = bot_api.analyze_farm(user_input)
except Exception as e:
    st.error(f"Error getting response: {str(e)}")
    # Fall back to mock
    bot_response = MockBotResponses.crop_health_analysis()
```

### API Contract

Your backend should return JSON matching this structure:

```json
{
  "message_id": "unique-id",
  "timestamp": "2025-01-09T10:30:00Z",
  "message_type": "insights",
  "text": "Your analysis",
  "insights": [
    {
      "label": "Metric",
      "value": "123",
      "unit": "unit",
      "trend": "up",
      "color": "green"
    }
  ],
  "charts": [
    {
      "type": "line",
      "title": "Chart Title",
      "data": {
        "x": ["A", "B"],
        "y": [1, 2]
      }
    }
  ],
  "recommendations": ["Action 1", "Action 2"],
  "alert": {
    "type": "warning",
    "message": "Alert message"
  },
  "metadata": {
    "source": "api",
    "confidence": 0.95
  }
}
```

---

## 📊 Adding Real-Time Data Updates

```python
# Add to app.py
import streamlit as st
from datetime import datetime, timedelta

# Initialize auto-refresh
if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now()

# Auto-refresh every 5 minutes
if datetime.now() - st.session_state.last_update > timedelta(minutes=5):
    st.rerun()
    st.session_state.last_update = datetime.now()
```

---

## 🔐 Adding Authentication

```python
# In app.py (top of file)
import streamlit as st

def check_authentication():
    """Check if user is authenticated"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.markdown("## 🔐 Login Required")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            username = st.text_input("Username")
        with col2:
            password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            # Verify credentials (replace with real auth)
            if username == "demo" and password == "password":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid credentials")
        
        st.stop()
    
    # Show logout button in sidebar
    with st.sidebar:
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

# Call at the top of main flow
check_authentication()
```

---

## 📈 Adding Analytics

```python
# In chat_manager.py
import json
from datetime import datetime

class AnalyticsLogger:
    """Log user interactions for analytics"""
    
    @staticmethod
    def log_message(role: str, content: str, message_type: str = "text"):
        """Log message to analytics"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "message_type": message_type,
            "content_length": len(str(content))
        }
        
        # Save to file or database
        with open("analytics.jsonl", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    @staticmethod
    def get_session_stats():
        """Get statistics for current session"""
        history = ChatManager.get_history()
        total_messages = len(history)
        user_messages = sum(1 for m in history if m["role"] == "user")
        bot_messages = total_messages - user_messages
        
        return {
            "total_messages": total_messages,
            "user_messages": user_messages,
            "bot_messages": bot_messages,
            "avg_response_length": sum(
                len(str(m["content"])) for m in history if m["role"] == "bot"
            ) // max(bot_messages, 1)
        }
```

---

## 🎓 Best Practices

### Code Organization
✅ Keep components focused and single-purpose
✅ Use type hints throughout
✅ Add docstrings to all functions
✅ Follow PEP 8 style guidelines

### Performance
✅ Cache expensive operations
✅ Use Streamlit caching with `@st.cache_data`
✅ Lazy load large datasets
✅ Optimize chart rendering

### Testing
✅ Test components independently
✅ Validate JSON responses match schema
✅ Test error cases and fallbacks
✅ Performance test with load tools

### Security
✅ Validate all user inputs
✅ Sanitize data before display
✅ Use HTTPS for API calls
✅ Never log sensitive data
✅ Implement rate limiting

### Maintainability
✅ Document API contracts clearly
✅ Use meaningful variable names
✅ Keep functions small (<30 lines)
✅ Extract magic strings to constants
✅ Version your API contract

---

## 🚀 Deployment

### Local Testing
```bash
streamlit run app.py
```

### Streamlit Cloud
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy from repo
4. Set environment variables

### Docker
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

### Environment Variables
```bash
# .streamlit/secrets.toml
API_URL = "https://your-api.com"
API_KEY = "your-secret-key"
DATABASE_URL = "postgresql://..."
```

---

## 📚 Additional Resources

### Streamlit
- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Components Gallery](https://streamlit.io/components)
- [Streamlit Cheat Sheet](https://docs.streamlit.io/library/cheatsheet)

### Plotly
- [Plotly Python Documentation](https://plotly.com/python)
- [Plotly Chart Gallery](https://plotly.com/python/gallery)
- [Plotly Configuration](https://plotly.com/python/configuration-options)

### Python
- [Type Hints](https://docs.python.org/3/library/typing.html)
- [Dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [Enums](https://docs.python.org/3/library/enum.html)

---

**Happy developing! 🚀**

If you have questions or find issues, check the main README.md and ARCHITECTURE.md files.
