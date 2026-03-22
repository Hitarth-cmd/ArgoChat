# AgroChat - Testing Commands Guide

## Quick Commands (Click in Sidebar)

These are pre-configured buttons in the left sidebar that automatically fill the input field:

1. **Soil Analysis** → "Show me soil health metrics for field A"
2. **Yield Forecast** → "What's my yield prediction for 2025?"
3. **Pest Activity** → "Where are pest hotspots in my fields?"
4. **Irrigation Plan** → "How much water should I apply this week?"
5. **Weather Alert** → "What's the weather forecast?"

---

## What Each Response Type Shows

### 1. Soil Moisture Trend (Time Series Chart)
**Command:** "Soil Analysis" or any message
**What you'll see:**
- Line chart with 30-day soil moisture data
- Blue line with markers showing daily readings
- X-axis: Dates, Y-axis: Moisture percentage (%)
- Shows trend from 46% → 55% moisture

---

### 2. Soil Nutrients Analysis (Metric Cards)
**Command:** Send any message (randomly selected)
**What you'll see:**
- 4 metric cards showing:
  - **Nitrogen (N)**: 85 mg/kg (Good)
  - **Phosphorus (P)**: 24 mg/kg (Fair)
  - **Potassium (K)**: 165 mg/kg (Good)
  - **pH Level**: 6.8 (Excellent)
- Each card has colored badge (green/yellow/red)
- Shows insight text below

---

### 3. Pest Distribution Map
**Command:** "Pest Activity" or send message
**What you'll see:**
- Interactive map with markers
- 6 pest hotspot locations with:
  - **Red markers** (Critical): High pest concentration
  - **Orange markers** (Medium): Moderate pest presence
  - **Yellow markers** (Low): Low risk areas
- Click markers to see details
- Shows percentage affected per area

---

### 4. Yield Prediction Comparison (Complex Response)
**Command:** "Yield Forecast" or send message
**What you'll see:**
- **Text explanation** at top
- **Bar chart** comparing:
  - Current year vs. predicted yield
  - Field A vs. Field B vs. Field C
- **Recommendation cards** with actions
- **Metadata** showing confidence level

---

### 5. Error Response (Alert/Warning)
**Command:** Send any message (randomly selected)
**What you'll see:**
- Red/orange alert box with warning icon
- Error message: "Weather Service Temporarily Unavailable"
- Technical details in expandable section
- Suggested actions:
  - "Check back in 1 hour"
  - "Use historical weather data"
  - "Contact support"

---

### 6. Irrigation Recommendation (Complex + Recommendations)
**Command:** "Irrigation Plan" or send message
**What you'll see:**
- **Text summary** explaining irrigation needs
- **Metric cards** showing water requirements
- **Line chart** showing daily irrigation schedule
- **Recommendation list** with numbered actions:
  1. "Apply 2.5cm water tomorrow morning"
  2. "Check soil moisture before irrigating"
  3. "Monitor forecast for rain"
  4. "Adjust nozzle pressure to 40 PSI"
  5. "Log irrigation event in system"

---

## Testing Tips

### Test All Chart Types
Each response contains different visualizations. Keep sending messages to see:
- ✅ Line charts (soil moisture)
- ✅ Bar charts (comparisons)
- ✅ Metric cards (insights)
- ✅ Maps with markers (locations)
- ✅ Error alerts (warnings)
- ✅ Recommendations (action items)

### Test UI Features

1. **Show Raw JSON**
   - Toggle "Show raw JSON" in sidebar
   - Click "View Raw JSON" expander on any response
   - See the actual JSON structure

2. **Response Type Filter**
   - Select "Charts" to get only chart responses
   - Select "Metrics" to get only insight cards
   - Select "Alerts" to get error messages
   - "All" shows everything

3. **Clear History**
   - Click "Clear History" button in sidebar
   - All messages reset
   - Start fresh conversation

4. **Message Timestamps**
   - Each message shows time (HH:MM format)
   - User messages on right (blue)
   - Bot messages on left (gray)

---

## Example Testing Session

```
1. Click "Soil Analysis" button
   → See soil moisture line chart with 30-day trend

2. Type: "Show yield data"
   → See bar chart comparing fields A, B, C

3. Click "Pest Activity" button
   → See interactive map with pest markers

4. Toggle "Show raw JSON" ON
   → See JSON structure in expanders

5. Select "Charts" in Response Type filter
   → Only chart responses shown

6. Click "Clear History"
   → Chat resets to welcome screen

7. Type: "weather"
   → Randomly get error alert response

8. Click "Irrigation Plan"
   → See irrigation schedule with recommendations
```

---

## Response Types in Sidebar Filter

| Filter | Shows | Example |
|--------|-------|---------|
| **All** | Any response | Everything |
| **Charts** | Line, bar, area charts | Soil moisture, yield comparison |
| **Metrics** | Insight cards | Nitrogen, pH, moisture values |
| **Recommendations** | Action items | Steps to take, improvements |
| **Alerts** | Errors, warnings | Weather service down |
| **Complex** | Multiple components | Yield prediction + recommendations |

---

## What Each Quick Command Tests

| Button | Tests |
|--------|-------|
| **Soil Analysis** | Metric cards (insights) |
| **Yield Forecast** | Complex (chart + recommendations) |
| **Pest Activity** | Map with markers |
| **Irrigation Plan** | Complex (chart + recommendations) |
| **Weather Alert** | Alerts/errors (may show success or error) |

---

## Technical Details

### Mock Response Sources
All responses come from `mock_bot_responses.py`:
- `time_series_soil_moisture()` - 30-day line chart
- `depth_profile_soil_nutrients()` - 4 metric cards
- `map_pest_distribution()` - 6 map markers with severities
- `comparison_yield_prediction()` - bar chart + recommendations
- `error_weather_service_down()` - error alert
- `irrigation_recommendation()` - complex with schedule

### Response Selection
The app randomly picks from all 6 responses each time you send a message, unless you filter by type in the sidebar.

---

## Troubleshooting

**Issue:** Maps not showing?
→ Check browser console, ensure pydeck is installed

**Issue:** Charts appear blank?
→ Check sidebar toggle "Show raw JSON" to see data structure

**Issue:** No recommendations showing?
→ Send another message to get "composite" or "recommendation" type response

**Issue:** Want specific response type?
→ Use sidebar filter "Response Types" dropdown

---

## Next Testing Steps

1. ✅ Test all chart types (line, bar)
2. ✅ Test metric cards (insights)
3. ✅ Test map markers (locations)
4. ✅ Test error handling (alerts)
5. ✅ Test recommendations (action items)
6. ✅ Test sidebar controls
7. 🔄 Ready to integrate real backend!

---

**Happy Testing! 🌾**
