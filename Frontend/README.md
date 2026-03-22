# 🌾 AgroChat - AI Farming Assistant Frontend

A **clean, modular Streamlit chatbot** demonstrating structured JSON-based bot responses with beautiful visualizations. This is a **frontend-only prototype** with zero backend dependencies.

## 🎯 Project Overview

- ✅ **Structured JSON Responses** - All bot replies follow a clean contract
- ✅ **Mock Bot Responses** - 8 different demo responses with realistic farm data
- ✅ **Beautiful Chat UI** - Native Streamlit chat interface with custom styling
- ✅ **Rich Visualizations** - Charts (Line, Bar, Area, Scatter, Gauge) using Plotly
- ✅ **Modular Architecture** - Backend-ready design with clear separation of concerns
- ✅ **Zero External APIs** - No database, no backend, no RAG, no ML models

## 📁 Project Structure

```
AgroChat/
├── app.py                 # Main Streamlit application
├── schemas.py             # JSON response contract & data models
├── mock_responses.py      # Mock bot responses with realistic data
├── components.py          # Rendering components for different response types
├── chat_manager.py        # Chat state management & message history
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🏗️ Architecture

### 1. **schemas.py** - Response Contract
Defines the clean JSON structure for all bot responses:

```python
BotResponse {
    message_id: str           # Unique message identifier
    timestamp: str            # ISO format timestamp
    message_type: str         # TEXT, CHART, INSIGHTS, ALERT, etc.
    
    # Main content
    text: Optional[str]       # Primary message
    
    # Rich content (optional)
    insights: List[InsightCard]           # Metrics & KPIs
    charts: List[ChartData]               # Plotly visualizations
    recommendations: List[str]             # Action items
    alert: Dict                           # Alert/notification
    
    # Metadata
    metadata: Dict            # Source info, confidence scores, etc.
}
```

**Example Response:**
```json
{
  "message_id": "abc12345",
  "timestamp": "2025-01-09T10:30:00Z",
  "message_type": "insights",
  "text": "Your crop health is excellent!",
  "insights": [
    {
      "label": "Soil Moisture",
      "value": "68",
      "unit": "%",
      "trend": "up",
      "color": "green"
    }
  ],
  "charts": [{
    "type": "line",
    "title": "Temperature Trend",
    "data": {"x": ["Mon", "Tue"], "y": [25, 26]}
  }],
  "recommendations": ["Increase irrigation by 15%"]
}
```

### 2. **mock_responses.py** - Demo Data
8 pre-built mock responses covering common farm scenarios:

| Response | Use Case |
|----------|----------|
| `greeting()` | Initial welcome message |
| `crop_health_analysis()` | Soil metrics, moisture, nitrogen, pest risk |
| `weather_forecast()` | 7-day temp & rainfall charts |
| `soil_analysis()` | Nutrient profile, pH, organic matter |
| `pest_alert()` | Pest detection warnings |
| `crop_recommendation()` | Seasonal crop suggestions |
| `market_prices()` | Commodity price trends |
| `equipment_maintenance()` | Equipment service reminders |

Each response includes:
- ✅ Multiple insight cards
- ✅ 1-2 Plotly charts
- ✅ Actionable recommendations
- ✅ Alerts/notifications
- ✅ Metadata with source info

### 3. **components.py** - Rendering Engine
Modular components for rendering different response types:

```python
ResponseRenderer.render_full_response(bot_response)
  ├── render_alert()           # Red/yellow/green alerts
  ├── render_text()            # Markdown text
  ├── render_insights()        # Metric cards in columns
  ├── render_charts()          # Plotly visualizations
  └── render_recommendations() # Bulleted recommendations
```

**Chart Types Supported:**
- 📈 **Line Charts** - Trends over time
- 📊 **Bar Charts** - Comparisons
- 📉 **Area Charts** - Stacked values
- 🔵 **Scatter Charts** - Correlations
- ⚙️ **Gauge Charts** - Single metrics
- 🗺️ **Map Charts** - PyDeck (ready for integration)

### 4. **chat_manager.py** - State Management
Handles chat history and message flow:

```python
ChatManager.init_session_state()        # Initialize Streamlit session
ChatManager.add_user_message(text)      # Add user input
ChatManager.add_bot_message(response)   # Add bot response
ChatManager.get_history()               # Retrieve chat history
ChatManager.clear_history()             # Reset chat
```

### 5. **app.py** - Main Application
Streamlit UI orchestrating the entire chat flow:

```
┌─────────────────────────────────────┐
│   Title: 🌾 AgroChat               │
├─────────────┬───────────────────────┤
│             │                       │
│  SIDEBAR    │   MAIN CHAT AREA     │
│             │                       │
│ • Quick     │  Chat History        │
│   Commands  │  ────────────────    │
│ • Options   │  User: Hi there!     │
│ • About     │  Bot: [$response]    │
│             │       [Charts]       │
│             │       [Insights]     │
│             │  User Input Box      │
└─────────────┴───────────────────────┘
```

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
# Run Streamlit app
streamlit run app.py

# App opens at http://localhost:8501
```

### Testing

Try these commands in the chat:

1. **"Crop health"** → Shows soil metrics + recommendations
2. **"Weather"** → 7-day forecast with charts
3. **"Soil analysis"** → Nutrient breakdown
4. **"Pest alert"** → Pest detection warning
5. **"Market prices"** → Commodity trends
6. **"Recommendations"** → Crop suggestions
7. **"Equipment"** → Maintenance reminders

Or use the **Quick Commands** buttons in the sidebar! 👈

## 🎨 UI Features

### Chat Interface
- ✅ Native Streamlit chat bubbles (user/bot)
- ✅ Emoji avatars (👨‍🌾 user, 🤖 bot)
- ✅ Message history persistence
- ✅ Clean message rendering

### Visualizations
- ✅ Colored metric cards with trend indicators (📈📉➡️)
- ✅ Responsive Plotly charts (light/dark mode compatible)
- ✅ Multi-column layouts
- ✅ Custom color schemes

### Sidebar
- ✅ 8 quick command buttons
- ✅ Clear history option
- ✅ View raw JSON toggle (for backend devs)
- ✅ About section with project info

## 📊 Example Response Breakdown

**User Input:** "How's my crop health?"

**Bot Response Flow:**
```
┌─ Alert (if present)
│  └─ "Armyworm activity detected"
│
├─ Main Text
│  └─ "Your wheat crop is in excellent condition"
│
├─ Insight Cards (4 in a row)
│  ├─ Soil Moisture: 68% 📈
│  ├─ Soil pH: 6.8 ➡️
│  ├─ Nitrogen: 42 mg/kg 📉
│  └─ Pest Risk: Low ✓
│
├─ Charts (responsive grid)
│  └─ [Plotly Line/Bar/Area Charts]
│
└─ Recommendations (bulleted list)
   ├─ Increase nitrogen fertilization
   ├─ Monitor moisture levels
   ├─ Scout for aphids weekly
   └─ Plan irrigation for weekend
```

## 🔧 Backend Integration (Future)

This frontend is **ready for backend integration**:

### To Connect a Real Backend:

1. **Replace mock responses** in `mock_responses.py`:
```python
# Instead of:
response = MockBotResponses.crop_health_analysis()

# Do:
response = requests.post("https://your-api.com/analyze", 
                         json={"query": user_input}).json()
response = BotResponse(**response)  # Deserialize using schema
```

2. **No UI changes needed** - All rendering happens through the schema contract

3. **Scaling tips**:
   - Add streaming for long-running responses
   - Cache responses in Redis
   - Add authentication layer
   - Implement rate limiting
   - Log user queries for analytics

## 📝 JSON Response Examples

### 1️⃣ Text-Only Response
```json
{
  "message_id": "msg001",
  "timestamp": "2025-01-09T10:30:00Z",
  "message_type": "text",
  "text": "Weather looks good for planting this week!"
}
```

### 2️⃣ Insights + Recommendations
```json
{
  "message_id": "msg002",
  "timestamp": "2025-01-09T10:31:00Z",
  "message_type": "insights",
  "text": "Soil analysis complete",
  "insights": [
    {"label": "pH", "value": "6.8", "color": "green", "trend": "stable"}
  ],
  "recommendations": ["Apply phosphate fertilizer"]
}
```

### 3️⃣ Charts + Metadata
```json
{
  "message_id": "msg003",
  "timestamp": "2025-01-09T10:32:00Z",
  "message_type": "chart",
  "text": "7-day forecast",
  "charts": [{
    "type": "line",
    "title": "Temperature",
    "data": {"x": ["Mon", "Tue"], "y": [22, 24]}
  }],
  "metadata": {"source": "weather_api", "confidence": 0.92}
}
```

## 🛠️ Extensibility

### Add a New Response Type

1. **Define in `schemas.py`:**
```python
@dataclass
class MyNewResponse(BotResponse):
    custom_field: Optional[str] = None
```

2. **Create in `mock_responses.py`:**
```python
@staticmethod
def my_new_response() -> BotResponse:
    return BotResponse(
        message_id=get_uuid(),
        timestamp=get_timestamp(),
        message_type="custom",
        text="Custom response",
        custom_field="value"
    )
```

3. **Render in `components.py`:**
```python
@staticmethod
def render_custom(response: BotResponse) -> None:
    st.markdown(f"Custom: {response.custom_field}")
```

4. **Add to `app.py` keyword mapping:**
```python
"your_keyword": MyNewResponse.my_new_response
```

### Add a New Chart Type

1. Create rendering function in `components.py`:
```python
def render_map_chart(data: dict, title: str) -> None:
    # Use pydeck for interactive maps
    st.pydeck_chart(...)
```

2. Add to `ResponseRenderer.render_single_chart()`:
```python
elif chart.type == "map":
    render_map_chart(chart.data, chart.title)
```

## 📦 Dependencies

```
streamlit>=1.28.0         # Chat UI framework
plotly>=5.17.0            # Interactive charts
pydeck>=0.8.0             # Map visualizations
pandas>=2.0.0             # Data handling (optional)
```

## 📚 Code Quality

✅ **Type Hints** - Full type annotations throughout
✅ **Docstrings** - Comprehensive documentation
✅ **Modular Design** - Clear separation of concerns
✅ **Error Handling** - Graceful fallbacks
✅ **Session State** - Proper Streamlit state management
✅ **PEP 8** - Code follows Python standards

## 🎓 Learning Resources

- [Streamlit Docs](https://docs.streamlit.io/)
- [Plotly Python](https://plotly.com/python/)
- [PyDeck Documentation](https://pydeck.gl/)
- [JSON Schema](https://json-schema.org/)

## 🚀 Performance Notes

- ✅ No API calls (everything is mock data)
- ✅ Instant response rendering
- ✅ Lightweight session state (<1MB)
- ✅ Optimized Plotly charts
- ✅ Works offline

## 🔒 Data Privacy

⚠️ **This is a demo/frontend prototype**
- No real data storage
- No backend API calls
- No database connections
- All responses are mock data

## 📸 Features at a Glance

| Feature | Status | Details |
|---------|--------|---------|
| Chat Interface | ✅ | Native Streamlit UI |
| JSON Schema | ✅ | Structured contracts |
| Mock Responses | ✅ | 8 pre-built examples |
| Charts | ✅ | Line, Bar, Area, Scatter, Gauge |
| Insights | ✅ | Metric cards with trends |
| Alerts | ✅ | Error/Warning/Success |
| History | ✅ | Persistent chat log |
| Mobile Responsive | ✅ | Works on tablets/phones |
| Dark Mode | ✅ | Auto-detects system theme |
| PyDeck Maps | 🔄 | Ready for integration |

## 🎯 Next Steps

### To Make This Production-Ready:

1. **Add Real Backend**
   - Replace `MockBotResponses` with API calls
   - Add authentication & rate limiting
   - Implement WebSocket for real-time updates

2. **Enhance Features**
   - Add file uploads (CSV sensor data)
   - Implement voice input
   - Add export to PDF/CSV
   - Real-time notifications

3. **Performance**
   - Cache responses
   - Lazy load charts
   - Optimize for mobile

4. **Analytics**
   - Track user queries
   - Monitor response times
   - A/B test recommendations

## 📄 License

MIT License - Feel free to use and modify!

---

**Built with ❤️ using Streamlit, Plotly, and Python**

🌾 *Your AI farming assistant is ready to help!*
