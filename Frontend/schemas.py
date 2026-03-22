"""
JSON Response Contract for Chatbot
Defines the structure of all bot responses
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
from enum import Enum
import json


class ResponseType(Enum):
    """Types of bot responses"""
    TEXT = "text"
    CHART = "chart"
    INSIGHTS = "insights"
    RECOMMENDATION = "recommendation"
    ALERT = "alert"


class ChartType(Enum):
    """Supported chart types"""
    LINE = "line"
    BAR = "bar"
    AREA = "area"
    SCATTER = "scatter"
    GAUGE = "gauge"
    MAP = "map"


@dataclass
class ChartData:
    """Chart visualization data"""
    type: str  # ChartType value
    title: str
    data: Dict[str, Any]  # Plotly-ready data structure
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "title": self.title,
            "data": self.data
        }


@dataclass
class InsightCard:
    """Individual insight/metric card"""
    label: str
    value: str
    unit: Optional[str] = None
    trend: Optional[str] = None  # "up", "down", "stable"
    color: Optional[str] = None  # "green", "red", "blue", "orange"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "label": self.label,
            "value": self.value,
            "unit": self.unit,
            "trend": self.trend,
            "color": self.color
        }


@dataclass
class BotResponse:
    """Main bot response contract"""
    message_id: str
    timestamp: str
    message_type: str  # ResponseType value
    
    # Primary content
    text: Optional[str] = None
    
    # Optional rich content
    insights: Optional[List[InsightCard]] = None
    charts: Optional[List[ChartData]] = None
    recommendations: Optional[List[str]] = None
    alert: Optional[Dict[str, str]] = None  # {"type": "warning|error|success", "message": "..."}
    
    # Metadata
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict"""
        return {
            "message_id": self.message_id,
            "timestamp": self.timestamp,
            "message_type": self.message_type,
            "text": self.text,
            "insights": [i.to_dict() for i in self.insights] if self.insights else None,
            "charts": [c.to_dict() for c in self.charts] if self.charts else None,
            "recommendations": self.recommendations,
            "alert": self.alert,
            "metadata": self.metadata
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)


# Example of a complex response structure
RESPONSE_SCHEMA = {
    "message_id": "uuid-here",
    "timestamp": "2025-01-09T10:30:00Z",
    "message_type": "insights",
    "text": "Here's a summary of your crop health",
    "insights": [
        {
            "label": "Soil Moisture",
            "value": "65",
            "unit": "%",
            "trend": "down",
            "color": "blue"
        }
    ],
    "charts": [
        {
            "type": "line",
            "title": "Temperature Trend",
            "data": {
                "x": ["Mon", "Tue", "Wed"],
                "y": [25, 26, 24]
            }
        }
    ],
    "recommendations": [
        "Increase irrigation by 15%",
        "Check soil pH levels"
    ],
    "alert": {
        "type": "warning",
        "message": "Pest activity detected in adjacent fields"
    },
    "metadata": {
        "source": "soil_sensor_array",
        "confidence": 0.92
    }
}
