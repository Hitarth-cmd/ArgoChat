# 🚀 Quick Start Guide - AgroChat

## Installation & Running

```bash
# 1. Navigate to project directory
cd "C:\Users\hitar\OneDrive\Attachments\Desktop\SEM6\AgroChat"

# 2. Install dependencies (one time)
pip install -r requirements.txt

# 3. Run the Streamlit app
streamlit run app.py
```

App opens at: **http://localhost:8501**

---

## 🎯 Try These Commands

| Command | What It Does |
|---------|--------------|
| "Crop health" | Shows soil metrics, moisture, nutrients, pest risk |
| "Weather" | 7-day weather forecast with temperature & rainfall |
| "Soil analysis" | Detailed nutrient profile and recommendations |
| "Pest alert" | Pest detection warning with action items |
| "Market prices" | Commodity price trends and selling tips |
| "Recommendations" | What crops to plant next season |
| "Equipment" | Maintenance reminders for farm equipment |

**Or use the Quick Command buttons** in the left sidebar! 👈

---

## 📁 Project Files Explained

```
schemas.py          → Defines the JSON response structure
                      (BotResponse, InsightCard, ChartData)

mock_responses.py   → 8 different demo bot responses
                      (Crop health, Weather, Soil, etc.)

components.py       → Rendering functions for charts, 
                      insights, alerts, recommendations

chat_manager.py     → Chat history & state management
                      (Add/get/clear messages)

app.py              → Main Streamlit app that ties it all together
                      (UI layout, chat flow, keyword routing)

requirements.txt    → Python package dependencies
                      (streamlit, plotly, pydeck, pandas)

README.md           → Full documentation & architecture guide
```

---

## 🎨 What You'll See

### Chat Screen
```
Title: 🌾 AgroChat - Your AI Farming Assistant

Sidebar (Left):
├─ 🚀 Quick Commands (8 buttons)
├─ 📊 Chat Options
│  ├─ 🗑️ Clear History
│  └─ 📋 View Raw JSON
└─ ℹ️ About

Main Area (Center):
├─ Chat History
│  ├─ 👨‍🌾 User Messages
│  └─ 🤖 Bot Responses
│     ├─ Text
│     ├─ Metric Cards
│     ├─ Charts
│     ├─ Recommendations
│     └─ Alerts
└─ Chat Input Box
```

---

## 💡 Key Features

✅ **Structured JSON Responses**
- Every bot reply is a clean, parseable JSON object
- Ready for real backend integration
- Includes: text, charts, insights, recommendations, alerts

✅ **Beautiful Visualizations**
- Line charts (trends)
- Bar charts (comparisons)
- Area charts (stacked data)
- Metric cards (KPIs with trend arrows)
- Color-coded alerts

✅ **Smart Routing**
- Type "crop health" → Crop analysis response
- Type "weather" → Weather forecast response
- Type anything else → Default crop health response

✅ **Modular Code**
- Each component is independent
- Easy to add new response types
- Easy to connect real backend API

---

## 🔍 Understanding the Flow

### When You Type a Message:

```
User Input
    ↓
Keyword Matching (in app.py)
    ↓
Select Mock Response Function
    ↓
BotResponse Object Created (structured JSON)
    ↓
ResponseRenderer Processes It
    ├─ Render alert (if any)
    ├─ Render main text
    ├─ Render insight cards
    ├─ Render charts
    └─ Render recommendations
    ↓
Display in Chat UI
    ↓
Save to Chat History
```

---

## 📊 Example Response Structure

Every bot response has this structure:

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
  
  "charts": [
    {
      "type": "line",
      "title": "Temperature Trend",
      "data": {
        "x": ["Mon", "Tue", "Wed"],
        "y": [22, 24, 23]
      }
    }
  ],
  
  "recommendations": [
    "Increase irrigation by 15%",
    "Check soil pH levels"
  ],
  
  "alert": {
    "type": "warning",
    "message": "Pest activity detected nearby"
  },
  
  "metadata": {
    "source": "sensor_array",
    "confidence": 0.94
  }
}
```

---

## 🔗 Connecting a Real Backend

Currently using **mock responses**. To connect a real backend:

### Step 1: Modify `mock_responses.py`

Replace this:
```python
@staticmethod
def crop_health_analysis() -> BotResponse:
    return BotResponse(...)  # hardcoded mock data
```

With this:
```python
@staticmethod
def crop_health_analysis(user_input: str) -> BotResponse:
    # Call your real API
    response = requests.post(
        "https://your-backend.com/analyze",
        json={"query": user_input}
    )
    data = response.json()
    
    # Parse JSON into BotResponse using schema
    return BotResponse(**data)
```

### Step 2: Update `app.py`

Instead of:
```python
bot_response = MockBotResponses.crop_health_analysis()
```

Do:
```python
bot_response = MockBotResponses.crop_health_analysis(user_input)
```

### That's It!
- No UI changes needed
- All rendering stays the same
- Schema contract ensures compatibility

---

## 🐛 Troubleshooting

### Error: `ModuleNotFoundError: No module named 'streamlit'`
```bash
pip install -r requirements.txt
```

### Error: `UnicodeDecodeError` in terminal
```bash
# Just run the app in a fresh terminal:
streamlit run app.py
```

### Charts not showing
- Reload the page (Ctrl+R)
- Check browser console for errors
- Run `streamlit cache clear` if needed

### Chat history disappeared
- This is normal - it resets when you restart the app
- To persist, save to a database (future enhancement)

---

## 🎓 Code Examples

### Adding a New Mock Response

In `mock_responses.py`:

```python
@staticmethod
def my_new_response() -> BotResponse:
    return BotResponse(
        message_id=get_uuid(),
        timestamp=get_timestamp(),
        message_type=ResponseType.TEXT.value,
        text="My custom response text",
        recommendations=[
            "Action 1",
            "Action 2"
        ]
    )
```

### Rendering it in the UI

In `app.py`, add to `response_map`:

```python
response_map = {
    "my_keyword": MockBotResponses.my_new_response,
    # ... other mappings
}
```

Now typing "my_keyword" will trigger your new response!

---

## 📚 Architecture Overview

```
┌─────────────────────────────────────────────┐
│         app.py (Main Streamlit App)        │
├─────────────────────────────────────────────┤
│                                             │
│  Sidebar            │      Main Chat        │
│  ──────────         │      ──────────       │
│  Quick Cmds   │     │  History Display      │
│  Options      │     │  + Rendering          │
│  About        │     │  ──────────────       │
│              │     │  Input Box            │
└──────────────┼─────┴─────────────────────────┘
               │
        Response Flow
        ──────────────
               │
        ┌──────┴──────────┐
        │                 │
    chat_manager.py    mock_responses.py
    ──────────────     ────────────────
    • Session State    • get_uuid()
    • Chat History     • get_timestamp()
    • Add Message      • crop_health_analysis()
    • Get History      • weather_forecast()
                       • soil_analysis()
                       • pest_alert()
                       • etc...
        │                 │
        └─────────┬───────┘
                  │
            ┌─────┴──────────┐
            │                │
          schemas.py    components.py
          ──────────     ────────────
          • BotResponse  • ResponseRenderer
          • InsightCard  • render_insights()
          • ChartData    • render_charts()
                         • render_alert()
                         • Plotly functions
```

---

## ✨ Cool Features to Explore

1. **Toggle Raw JSON View**
   - Click "View Raw JSON" in sidebar
   - See exact structure of every response
   - Perfect for backend integration planning

2. **Quick Commands**
   - One-click demo responses
   - Great for testing different scenarios
   - No typing needed!

3. **Chart Types**
   - Line (trends), Bar (comparison)
   - Area (composition), Scatter (correlation)
   - Gauge (single metrics)

4. **Insight Cards**
   - Color-coded (green/orange/red)
   - Trend indicators (📈📉➡️)
   - Organized in responsive grid

5. **Alert System**
   - Error (red), Warning (yellow), Success (green)
   - Always displayed prominently
   - Perfect for urgent notifications

---

## 🚀 Next Steps

1. ✅ **Run the app** - `streamlit run app.py`
2. ✅ **Click Quick Commands** - Try different responses
3. ✅ **Type custom queries** - Test keyword matching
4. ✅ **Click "View Raw JSON"** - See response structure
5. ✅ **Read the code** - Understand modular design
6. ✅ **Plan backend** - Design API to match schema
7. ✅ **Integrate API** - Replace mock with real responses

---

## 📞 Support

- Check README.md for detailed documentation
- Review code comments for implementation details
- All functions have docstrings explaining usage

---

**Happy Farming! 🌾**

*This chatbot is ready for production. Just connect your backend!*
