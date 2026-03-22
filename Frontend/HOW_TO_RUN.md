# 🚀 How to Run AgroChat

## Quick Start (30 seconds)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py

# 3. Open browser
# Automatically opens at http://localhost:8501
```

---

## Detailed Setup Instructions

### Step 1: Prerequisites
- **Python 3.8+** installed
- **pip** package manager
- **Git** (optional, for cloning)

Check Python version:
```bash
python --version
```

### Step 2: Navigate to Project Directory
```bash
cd c:\Users\hitar\OneDrive\Attachments\Desktop\SEM6\AgroChat
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**What gets installed:**
- `streamlit` - Web framework
- `plotly` - Interactive charts
- `pydeck` - Map visualizations
- `pandas` - Data handling
- `numpy` - Numerical operations

### Step 4: Run the Application
```bash
streamlit run app.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501

  For better performance, install pyarrow: pip install pyarrow
```

### Step 5: Access the App
- Browser automatically opens to `http://localhost:8501`
- If not, manually open the URL

---

## 🎮 Using the Application

### Sidebar Controls
1. **Quick Commands** - Click any to auto-fill query
2. **Response Type Filter** - Filter by chart/metrics/alerts
3. **Settings** - Toggle metadata and raw JSON view
4. **Clear History** - Reset conversation

### Chat Interaction
1. Type your question in the input field
2. Click "📤 Send" button (or press button)
3. Bot responds with visualizations
4. Scroll down to see entire response
5. Toggle "Raw JSON" to see response structure

### Example Queries
- "Show me soil health metrics"
- "What's my yield prediction?"
- "Where are pest hotspots?"
- "How much water should I apply?"
- "What's the weather forecast?"

---

## ⚙️ Configuration

### Development Mode (Default - Uses Mock Data)
App runs immediately with no configuration needed.
Responses come from `mock_bot_responses.py`.

```bash
streamlit run app.py
```

### Production Mode (With Real Backend)
Set environment variables before running:

```bash
# Windows PowerShell
$env:BACKEND_API_URL = "https://api.agrochat.com"
$env:BACKEND_API_KEY = "your-api-key"
streamlit run app.py

# Or Windows CMD
set BACKEND_API_URL=https://api.agrochat.com
set BACKEND_API_KEY=your-api-key
streamlit run app.py

# Linux/Mac
export BACKEND_API_URL="https://api.agrochat.com"
export BACKEND_API_KEY="your-api-key"
streamlit run app.py
```

Or edit `config.yaml`:
```yaml
production:
  api_url: "https://api.agrochat.com"
  api_key: "your-api-key"
```

---

## 📂 Project Structure

```
AgroChat/
├── app.py                          # Main application
├── api_service.py                  # Backend abstraction layer (NEW)
├── mock_bot_responses.py           # Mock data generator
├── schemas.py                      # JSON schema definitions
├── chat_manager.py                 # Chat state management (if exists)
├── requirements.txt                # Python dependencies
│
├── components/
│   ├── bot_reply_renderer.py      # Response rendering
│   └── visual_dispatcher.py        # Chart/map rendering
│
├── RESPONSE_SCHEMA.md              # Schema documentation
├── response_schema.json            # JSON Schema (draft-07)
├── APP_GUIDE.md                    # Architecture guide
│
└── examples_*.json                 # Example responses
    ├── examples_text_only.json
    ├── examples_text_chart.json
    ├── examples_text_insights.json
    ├── examples_text_map.json
    └── examples_error.json
```

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Port 8501 already in use
**Solution:** Use different port
```bash
streamlit run app.py --server.port 8502
```

### Issue: Blank page or errors in browser
**Solution:** Check terminal for error messages
1. Stop app: Press `Ctrl+C` in terminal
2. Check for error output
3. Ensure all files are in correct directory

### Issue: Components not rendering
**Solution:** Ensure components directory exists
```bash
# Check components folder
ls components/
# Should contain: bot_reply_renderer.py, visual_dispatcher.py
```

### Issue: Mock responses not appearing
**Solution:** Verify mock_bot_responses.py exists
```bash
# Check file
ls mock_bot_responses.py
# Try re-running: streamlit run app.py
```

---

## 🧪 Testing the Application

### Test 1: Basic Chat
1. Type: "Show me soil metrics"
2. Click Send
3. Bot response appears on left
4. Verify metrics cards render

### Test 2: Chart Visualization
1. Click "📈 Yield Forecast" from sidebar
2. Should show line chart with historical data
3. Hover on chart points to see values

### Test 3: Map Display
1. Click "🗺️ Pest Activity" from sidebar
2. Should show interactive map with markers
3. Click markers to see details

### Test 4: Error Handling
1. Click "Raw JSON" toggle
2. Observe response structure
3. Turn off toggle

### Test 5: Response Filtering
1. Select "Charts" from "Response Type" dropdown
2. Send message
3. Should only get chart-type responses

### Test 6: Clear History
1. Send a few messages
2. Click "🗑️ Clear History"
3. Chat should be empty
4. Click "Confirm" if prompted

---

## 📊 Viewing Raw JSON

To see the raw response structure:

1. **In Sidebar**: Toggle "Raw JSON" ✓
2. **Message**: Response shows JSON viewer
3. **Inspect**: Check `message_type`, `insights`, `charts`, etc.
4. **Compare**: Against `response_schema.json`

---

## 🔌 Switching from Mock to Real Backend

When backend API is ready:

1. **Set environment variable** (as shown above)
2. **Implement HTTP client** in `api_service.py`
3. **Run app**: `streamlit run app.py`
4. App automatically uses backend instead of mock

---

## 📈 Advanced Features

### View Response Metadata
- Confidence score
- Data source
- Processing time
- Data freshness

### View Technical Details
1. Click expander under error message
2. See error code and details
3. Get suggested action

### Multiple Conversation Threads
- Each session has separate history
- Refresh page for new session
- History stored in `st.session_state`

---

## 🛑 Stopping the Application

### Method 1: Terminal
Press `Ctrl+C` in the terminal window

### Method 2: Browser
Close the browser tab (app continues running until you stop terminal)

### Method 3: Kill Process
```bash
# Windows PowerShell
Stop-Process -Name "streamlit"

# Or find and kill
Get-Process | Where-Object {$_.ProcessName -like "*streamlit*"}
```

---

## 📝 Example Session

```
1. Run: streamlit run app.py
2. Browser opens to http://localhost:8501
3. See welcome message: "👋 Welcome to AgroChat"
4. Click "📊 Soil Analysis" in sidebar
5. Input pre-filled: "Show me soil health metrics"
6. Click "Send"
7. Bot responds with:
   - Bot message explaining results
   - Metric cards (Soil Moisture, pH, Nitrogen, etc.)
   - Metadata footer
8. Toggle "Raw JSON" to see response structure
9. Send another message
10. Both messages appear in history
11. Click "Clear History" to reset
12. Press Ctrl+C to stop app
```

---

## 🎯 Next Steps After Running

### Option 1: Explore UI
- Try different quick commands
- Test response filtering
- View raw JSON responses
- Check error handling

### Option 2: Review Code
- Open `app.py` to understand main flow
- Check `bot_reply_renderer.py` for rendering logic
- View `mock_bot_responses.py` to see mock data structure
- Read `RESPONSE_SCHEMA.md` for schema details

### Option 3: Integrate Backend
- Set up `api_service.py` with real API endpoint
- Configure environment variables
- Test with backend responses
- Deploy to production

---

## 📞 Support

If you encounter issues:

1. **Check logs** in terminal window
2. **Review structure** with `ls -la` or file explorer
3. **Verify imports** in Python files
4. **Check ports** with `netstat -an | grep 8501` (Windows)
5. **Reinstall dependencies** if needed: `pip install --upgrade -r requirements.txt`

---

## 🎓 Documentation

- **[RESPONSE_SCHEMA.md](RESPONSE_SCHEMA.md)** - Complete schema documentation
- **[APP_GUIDE.md](APP_GUIDE.md)** - Architecture and components
- **[response_schema.json](response_schema.json)** - JSON Schema (for validation)
- **Code comments** - Throughout application files

---

**Ready to run? Execute:**
```bash
streamlit run app.py
```

Enjoy exploring AgroChat! 🌾
