# AgroChat Response Schema Documentation

## Overview
This document defines the complete JSON schema for all chatbot responses. The schema is designed to be:
- **Extensible**: Support new response types without breaking changes
- **Frontend-friendly**: Easy to parse and render in web/mobile apps
- **Semantic**: Clear structure enables rich visualizations
- **Validated**: Dataclass-based implementation with type hints

---

## Core Schema Structure

### Root Response Object

```typescript
{
  "message_id": string,           // UUID or timestamp-based ID (unique per response)
  "timestamp": string,             // ISO 8601 format (e.g., "2025-01-12T10:30:45Z")
  "message_type": string,          // Enum: "text" | "chart" | "insights" | "recommendation" | "alert" | "composite"
  "text": string | null,           // Primary text content
  "metadata": {                    // Optional metadata object
    "source": string,              // e.g., "ai_model", "database", "calculation"
    "confidence": number,          // 0.0 to 1.0
    "model_version": string,       // e.g., "v1.0"
    "processing_time_ms": number,  // milliseconds
    "data_freshness": string       // ISO 8601 duration (e.g., "PT5M" = 5 minutes ago)
  },
  "insights": InsightCard[] | null,       // Array of metric cards
  "charts": ChartVisualization[] | null,  // Array of chart definitions
  "recommendations": string[] | null,     // List of action items
  "location": MapData | null,             // Geographic data
  "alert": AlertInfo | null,              // Error/warning information
  "links": RelatedLink[] | null           // Related resources
}
```

---

## Component Schemas

### 1. InsightCard
Represents individual metrics or KPIs

```typescript
{
  "label": string,           // e.g., "Soil pH"
  "value": string,           // e.g., "7.2"
  "unit": string | null,     // e.g., "pH units", "%", "°C"
  "trend": string | null,    // Enum: "up" | "down" | "stable" | null
  "color": string | null,    // Enum: "green" | "red" | "yellow" | "blue" | "orange"
  "icon": string | null      // Icon name (e.g., "thermometer", "droplet", "leaf")
}
```

### 2. ChartVisualization
Plotly-compatible chart definitions

```typescript
{
  "type": string,            // Enum: "line" | "bar" | "area" | "scatter" | "gauge" | "pie" | "heatmap"
  "title": string,           // Chart title
  "description": string | null, // Optional description
  "data": {
    "x": (string | number)[],
    "y": (string | number)[],
    "mode": string | null,   // "lines", "markers", "lines+markers"
    "fill": string | null,   // "tozeroy", "tonexty"
    "name": string | null,   // Series name
    "color": string | null,  // RGB or hex color
    "[key: string]": any     // Plotly-specific properties
  },
  "layout": {
    "title": string,
    "xaxis": { "title": string, "[key: string]": any },
    "yaxis": { "title": string, "[key: string]": any },
    "hovermode": string,
    "[key: string]": any     // Additional layout options
  },
  "xaxis_label": string | null,  // e.g., "Days"
  "yaxis_label": string | null,  // e.g., "Temperature (°C)"
  "time_range": {
    "start": string,         // ISO 8601
    "end": string            // ISO 8601
  } | null
}
```

### 3. MapData
Geographic visualization

```typescript
{
  "type": "map",
  "title": string,
  "center": {
    "lat": number,
    "lon": number
  },
  "zoom": number,            // 1-18 (higher = more zoomed)
  "markers": {
    "lat": number,
    "lon": number,
    "label": string,
    "color": string | null,
    "popup": string | null   // HTML content
  }[] | null,
  "geojson": any | null,     // GeoJSON feature collection
  "layer_type": string,      // "satellite" | "terrain" | "street"
  "bounds": {
    "north": number,
    "south": number,
    "east": number,
    "west": number
  } | null
}
```

### 4. AlertInfo
Error and warning information

```typescript
{
  "type": string,            // Enum: "error" | "warning" | "info" | "success"
  "title": string,           // Alert title
  "message": string,         // Alert message
  "code": string | null,     // Error code (e.g., "E001")
  "details": string | null,  // Additional details
  "action": string | null,   // Suggested action (e.g., "Retry in 5 minutes")
  "timestamp": string        // ISO 8601
}
```

### 5. RelatedLink
Cross-reference and navigation

```typescript
{
  "text": string,            // Link text
  "url": string,             // URL
  "type": string | null,     // "documentation" | "related_query" | "support" | "external"
  "icon": string | null      // Icon identifier
}
```

---

## Response Type Patterns

### Pattern 1: Text Only
Simplest response type

```json
{
  "message_id": "msg_20250112_001",
  "timestamp": "2025-01-12T10:30:45Z",
  "message_type": "text",
  "text": "Your wheat field shows good growth. Current status is optimal for this time of year.",
  "metadata": {
    "source": "ai_model",
    "confidence": 0.92,
    "model_version": "v2.1",
    "processing_time_ms": 245
  }
}
```

---

### Pattern 2: Text + Time Series Chart
Trend visualization

```json
{
  "message_id": "msg_20250112_002",
  "timestamp": "2025-01-12T10:31:12Z",
  "message_type": "chart",
  "text": "Temperature trend over the last 7 days shows gradual increase. Average: 18.5°C",
  "charts": [
    {
      "type": "line",
      "title": "Field Temperature Trend",
      "description": "Hourly temperature readings from weather station",
      "data": {
        "x": ["2025-01-05", "2025-01-06", "2025-01-07", "2025-01-08", "2025-01-09", "2025-01-10", "2025-01-11"],
        "y": [15.2, 16.1, 16.8, 17.5, 18.2, 18.9, 19.4],
        "mode": "lines+markers",
        "fill": "tozeroy",
        "name": "Temperature",
        "color": "#FF6B6B"
      },
      "layout": {
        "title": "7-Day Temperature Trend",
        "hovermode": "x unified",
        "xaxis": {
          "title": "Date",
          "gridcolor": "#E0E0E0"
        },
        "yaxis": {
          "title": "Temperature (°C)",
          "gridcolor": "#E0E0E0"
        }
      },
      "xaxis_label": "Date",
      "yaxis_label": "Temperature (°C)",
      "time_range": {
        "start": "2025-01-05T00:00:00Z",
        "end": "2025-01-11T23:59:59Z"
      }
    }
  ],
  "metadata": {
    "source": "weather_api",
    "confidence": 0.98,
    "data_freshness": "PT30M",
    "processing_time_ms": 156
  }
}
```

---

### Pattern 3: Text + Insights (Metrics)
Multi-metric dashboard card

```json
{
  "message_id": "msg_20250112_003",
  "timestamp": "2025-01-12T10:32:00Z",
  "message_type": "insights",
  "text": "Health assessment for Field North-1. Overall condition is excellent.",
  "insights": [
    {
      "label": "Soil Moisture",
      "value": "65",
      "unit": "%",
      "trend": "stable",
      "color": "green",
      "icon": "droplet"
    },
    {
      "label": "Soil pH",
      "value": "7.2",
      "unit": "pH",
      "trend": "up",
      "color": "green",
      "icon": "flask"
    },
    {
      "label": "Nitrogen Level",
      "value": "142",
      "unit": "mg/kg",
      "trend": "down",
      "color": "yellow",
      "icon": "leaf"
    },
    {
      "label": "Crop Health Index",
      "value": "92",
      "unit": "%",
      "trend": "up",
      "color": "green",
      "icon": "heart"
    }
  ],
  "metadata": {
    "source": "database",
    "confidence": 0.95,
    "processing_time_ms": 89
  }
}
```

---

### Pattern 4: Text + Map
Geographic data visualization

```json
{
  "message_id": "msg_20250112_004",
  "timestamp": "2025-01-12T10:33:15Z",
  "message_type": "chart",
  "text": "Pest activity detected in the highlighted zones. Recommend targeted treatment in red areas.",
  "location": {
    "type": "map",
    "title": "Pest Activity Heatmap",
    "center": {
      "lat": 28.7041,
      "lon": 77.1025
    },
    "zoom": 14,
    "markers": [
      {
        "lat": 28.7041,
        "lon": 77.1025,
        "label": "High Activity Zone",
        "color": "red",
        "popup": "Severe infestation detected. Treatment recommended immediately."
      },
      {
        "lat": 28.7055,
        "lon": 77.1030,
        "label": "Moderate Activity",
        "color": "orange",
        "popup": "Moderate pest presence. Monitor closely."
      },
      {
        "lat": 28.7030,
        "lon": 77.1010,
        "label": "Low Activity",
        "color": "green",
        "popup": "Minimal pest presence. No action needed."
      }
    ],
    "layer_type": "satellite",
    "bounds": {
      "north": 28.715,
      "south": 28.693,
      "east": 77.115,
      "west": 77.090
    }
  },
  "metadata": {
    "source": "satellite_imagery",
    "confidence": 0.87,
    "data_freshness": "PT2H",
    "processing_time_ms": 2340
  }
}
```

---

### Pattern 5: Text + Recommendations
Action items and suggestions

```json
{
  "message_id": "msg_20250112_005",
  "timestamp": "2025-01-12T10:34:00Z",
  "message_type": "recommendation",
  "text": "Based on current conditions, I recommend the following actions for optimal harvest.",
  "recommendations": [
    "Increase irrigation by 15% due to low soil moisture (currently 45%)",
    "Apply nitrogen fertilizer (150 kg/hectare) - levels are 18% below optimal",
    "Scout for aphids in Field North-3 - favorable weather conditions detected",
    "Schedule harvesting for Field South-1 within 7-10 days for peak grain maturity",
    "Check drip irrigation system valves before next watering cycle"
  ],
  "metadata": {
    "source": "ai_model",
    "confidence": 0.88,
    "model_version": "v2.1",
    "processing_time_ms": 512
  }
}
```

---

### Pattern 6: Error Response
Failure and error handling

```json
{
  "message_id": "msg_20250112_006",
  "timestamp": "2025-01-12T10:35:22Z",
  "message_type": "alert",
  "text": "Unable to fetch current weather data. Showing cached data from 2 hours ago.",
  "alert": {
    "type": "error",
    "title": "Weather API Unavailable",
    "message": "Connection to weather service failed. The system will retry in 5 minutes.",
    "code": "ERR_API_TIMEOUT",
    "details": "Request timed out after 30 seconds. Status: 504 Gateway Timeout",
    "action": "Retry or use cached data",
    "timestamp": "2025-01-12T10:35:22Z"
  },
  "metadata": {
    "source": "error_handler",
    "confidence": null,
    "processing_time_ms": 31000
  }
}
```

---

### Pattern 7: Composite Response (Multiple Components)
Complex response with multiple visualizations

```json
{
  "message_id": "msg_20250112_007",
  "timestamp": "2025-01-12T10:36:00Z",
  "message_type": "composite",
  "text": "Comprehensive health report for Farm A. See metrics, trend analysis, and recommendations below.",
  "insights": [
    {
      "label": "Yield Prediction",
      "value": "8.5",
      "unit": "tons/hectare",
      "trend": "up",
      "color": "green",
      "icon": "sprout"
    },
    {
      "label": "Water Efficiency",
      "value": "78",
      "unit": "%",
      "trend": "stable",
      "color": "green",
      "icon": "water"
    }
  ],
  "charts": [
    {
      "type": "line",
      "title": "Crop Growth Index",
      "data": {
        "x": ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5"],
        "y": [45, 52, 61, 73, 85],
        "mode": "lines+markers",
        "name": "Growth Index"
      },
      "layout": {
        "title": "5-Week Growth Progression",
        "hovermode": "x unified"
      }
    }
  ],
  "recommendations": [
    "Continue current watering schedule",
    "Apply pest control treatment if threshold breached"
  ],
  "links": [
    {
      "text": "View detailed analytics",
      "url": "/analytics/farm-a",
      "type": "related_query"
    },
    {
      "text": "Contact agronomist",
      "url": "mailto:expert@agrochat.com",
      "type": "support"
    }
  ],
  "metadata": {
    "source": "ai_model",
    "confidence": 0.91,
    "model_version": "v2.1",
    "processing_time_ms": 1250
  }
}
```

---

## Frontend Implementation Guide

### Parsing Strategy
```javascript
// Pseudo-code for frontend parsing
function renderBotResponse(response) {
  // 1. Always render text content if present
  if (response.text) renderText(response.text);
  
  // 2. Render content based on message_type
  switch(response.message_type) {
    case 'text':
      // Already rendered above
      break;
    case 'chart':
      if (response.charts) response.charts.forEach(renderChart);
      if (response.location) renderMap(response.location);
      break;
    case 'insights':
      renderInsightCards(response.insights);
      break;
    case 'recommendation':
      renderRecommendationsList(response.recommendations);
      break;
    case 'alert':
      renderAlert(response.alert);
      break;
    case 'composite':
      // Render all components
      if (response.insights) renderInsightCards(response.insights);
      if (response.charts) response.charts.forEach(renderChart);
      if (response.recommendations) renderRecommendationsList(response.recommendations);
      break;
  }
  
  // 3. Optionally render metadata in footer
  if (response.metadata) renderMetadataFooter(response.metadata);
  
  // 4. Optionally render related links
  if (response.links) renderLinks(response.links);
}
```

### Validation
```javascript
// Use JSON Schema validation library (e.g., jsonschema, ajv)
const validate = ajv.compile(BotResponseSchema);
if (!validate(response)) {
  console.error('Invalid response:', validate.errors);
  return fallbackResponse;
}
```

---

## Backward Compatibility & Extensibility

### Adding New Response Types
To add a new response type (e.g., `"video"`, `"table"`, `"form"`):

1. Add to `ResponseType` enum in `schemas.py`
2. Create corresponding dataclass (e.g., `VideoData`)
3. Add to `BotResponse` dataclass as optional field
4. Update frontend switch statement
5. No breaking changes to existing responses ✅

### Future Extensions
- `"table"` - Structured data in rows/columns
- `"form"` - Interactive input forms
- `"video"` - Embedded video content
- `"gallery"` - Image carousel
- `"timeline"` - Historical timeline
- `"comparison"` - Side-by-side metrics

---

## Validation Rules

| Field | Required | Type | Constraints |
|-------|----------|------|-------------|
| `message_id` | ✅ | string | Must be unique per response |
| `timestamp` | ✅ | string | ISO 8601 format |
| `message_type` | ✅ | string | Must match ResponseType enum |
| `text` | ❌ | string | Max 5000 characters |
| `metadata.confidence` | ❌ | number | 0.0 - 1.0 (inclusive) |
| `insights[].value` | ✅ | string | Any numeric/text representation |
| `charts[].data.x` | ✅ | array | Same length as `y` |
| `charts[].data.y` | ✅ | array | Same length as `x` |
| `alert.type` | ✅ | string | "error", "warning", "info", "success" |

---

## Example Use Cases

### Use Case 1: Weather Advisory
```json
{
  "message_type": "composite",
  "text": "Rain incoming - prepare irrigation",
  "charts": [{"type": "bar", "title": "Rainfall Forecast"}],
  "recommendations": ["Reduce irrigation", "Check drainage"],
  "metadata": {"source": "weather_api", "confidence": 0.94}
}
```

### Use Case 2: Disease Detection
```json
{
  "message_type": "alert",
  "text": "Early blight detected in field zone 3",
  "alert": {"type": "warning", "title": "Disease Alert"},
  "location": {"type": "map", "markers": [...]},
  "metadata": {"source": "satellite_imagery", "confidence": 0.87}
}
```

### Use Case 3: Harvest Readiness
```json
{
  "message_type": "insights",
  "text": "Your wheat field is 95% ready for harvest",
  "insights": [
    {"label": "Grain Moisture", "value": "14.2", "unit": "%", "trend": "down"},
    {"label": "Maturity Index", "value": "98", "unit": "%", "color": "green"}
  ]
}
```

---

## Summary

This schema provides:
- ✅ **Clear contract** between backend and frontend
- ✅ **Type safety** via Python dataclasses
- ✅ **Extensibility** without breaking changes
- ✅ **Rich visualizations** (charts, maps, metrics)
- ✅ **Error handling** with detailed messages
- ✅ **Metadata** for traceability and debugging
- ✅ **Frontend-friendly** parsing patterns
