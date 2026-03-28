import xarray as xr
import pandas as pd
import json
import httpx
from pathlib import Path
from typing import Dict, Any, Tuple

class OceanProcessor:
    def __init__(self, nc_file_path: str = None):
        """Initialize the OceanProcessor with a NetCDF file."""
        if nc_file_path is None:
            nc_file_path = str(Path(__file__).parent / "data" / "ocean_data.nc")
        self.nc_file_path = nc_file_path
        
        # Load dataset lazily
        try:
            self.ds = xr.open_dataset(self.nc_file_path)
            print(f"Loaded ocean dataset from {self.nc_file_path}")
        except Exception as e:
            print(f"Error loading NetCDF file: {e}")
            self.ds = None

    async def extract_query_json(self, query: str, base_url: str = "http://localhost:11434") -> Dict[str, Any]:
        """Uses Ollama to convert a natural language query into JSON."""
        system_prompt = '''You are an intelligent routing and data interpretation AI.

Your job is to analyze the user's query and decide whether it requires:

1. A textual response (RAG / knowledge-based answer)
2. A data visualization (chart/graph)

---

STRICT RULES:

* ALWAYS return ONLY valid JSON
* DO NOT explain anything
* DO NOT add extra text
* DO NOT use markdown
* Output must be directly parsable

---

STEP 1: Determine intent

If the query involves:

* trends, charts, graphs, plots, visualization
* time-series data (e.g., "from 2010 to 2025")
* comparisons across years or regions

→ intent = "data"

Otherwise:
→ intent = "rag"

---

STEP 2: Output format

IF intent = "rag":

{
"intent": "rag",
"query": "<original user query>"
}

---

IF intent = "data":

Extract the following:

* variable (temperature, salinity, pressure, etc.)
* start_year
* end_year
* region (Indian Ocean, Pacific Ocean, global, etc.)
* operation (trend, average, min, max, comparison)
* chart_type (line, bar, scatter, heatmap)
* aggregation (yearly, monthly, spatial)

---

Return:

{
"intent": "data",
"variable": "",
"start_year": 0,
"end_year": 0,
"region": "",
"operation": "",
"chart_type": "",
"aggregation": ""
}

---

EXAMPLES:

User Query:
"What is ocean temperature?"

Output:
{
"intent": "rag",
"query": "What is ocean temperature?"
}

---

User Query:
"Show salinity trend from 2015 to 2025 as a bar chart"

Output:
{
"intent": "data",
"variable": "salinity",
"start_year": 2015,
"end_year": 2025,
"region": "global",
"operation": "trend",
"chart_type": "bar",
"aggregation": "yearly"
}

---

User Query:
"Compare temperature between 2010 and 2020 in Indian Ocean"

Output:
{
"intent": "data",
"variable": "temperature",
"start_year": 2010,
"end_year": 2020,
"region": "Indian Ocean",
"operation": "comparison",
"chart_type": "line",
"aggregation": "yearly"
}'''
        
        prompt = f"{system_prompt}\n\nUser Query: {query}"
        
        payload = {
            "model": "phi3",
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.0,
                "num_ctx": 1024
            }
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(f"{base_url}/api/generate", json=payload)
                response.raise_for_status()
                data = response.json()
                text = data.get("response", "").strip()
                
                # Robust extraction: find the first { and last }
                import re
                match = re.search(r'\{.*\}', text, re.DOTALL)
                if match:
                    json_str = match.group(0)
                    return json.loads(json_str)
                else:
                    raise ValueError("No JSON dictionary found in response.")
                    
            except Exception as e:
                print(f"JSON Parsing Error: {e}")
                q_low = query.lower()
                
                # Smart fallback: if the query clearly asks for data visualization
                if any(k in q_low for k in ["chart", "trend", "average", "plot", "graph"]):
                    print("Fallback triggered: Detected data request keywords, forcing generic data intent.")
                    return {
                        "intent": "data",
                        "variable": "temperature",
                        "start_year": 2015,
                        "end_year": 2025,
                        "region": "Indian Ocean",
                        "operation": "trend" if "trend" in q_low else "average",
                        "chart_type": "line"
                    }

                # Default RAG Fallback
                return {
                    "intent": "rag",
                    "query": query
                }

    def process_data(self, params: Dict[str, Any]) -> Tuple[Dict, str]:
        """Filter xarray dataset based on parameters and compute the operation."""
        if self.ds is None:
            return {}, "Ocean dataset not available."
            
        start_year = str(params.get("start_year", 2010))
        end_year = str(params.get("end_year", 2025))
        variable = params.get("variable", "temperature").lower()
        operation = params.get("operation", "average").lower()
        region = params.get("region", "Indian Ocean")
        
        # Simple region bounding box mapping (mocking)
        # Indian Ocean broadly: Lat -40 to 30, Lon 30 to 110 (which is our entire dataset)
        lat_slice = slice(-40, 30)
        lon_slice = slice(30, 110)
        
        # Select target variable(s)
        var_keys = ["temperature", "salinity"] if variable == "both" else [variable]
        for v in var_keys:
            if v not in self.ds.data_vars:
                return {}, f"Variable '{v}' not found in dataset."
                
        # Slice by time and space
        subset = self.ds[var_keys].sel(
            time=slice(f"{start_year}-01-01", f"{end_year}-12-31"),
            latitude=lat_slice,
            longitude=lon_slice
        )
        
        chart_data = {"times": [], "values": [], "variable": variable, "operation": operation, "title": f"{operation.title()} {variable.title()} in {region} ({start_year}-{end_year})"}
        text_response = f"Analyzed {variable} data for the {region} from {start_year} to {end_year}. "
        
        try:
            # Time series aggregation over space (lat, lon)
            if operation == "average":
                timeseries = subset.mean(dim=["latitude", "longitude"])
                val = float(timeseries.mean().to_array().mean())
                text_response += f"The overall spatial and temporal average was {val:.2f}."
            elif operation == "max":
                timeseries = subset.max(dim=["latitude", "longitude"])
                val = float(timeseries.max().to_array().max())
                text_response += f"The absolute maximum observed was {val:.2f}."
            elif operation == "min":
                timeseries = subset.min(dim=["latitude", "longitude"])
                val = float(timeseries.min().to_array().min())
                text_response += f"The absolute minimum observed was {val:.2f}."
            elif operation == "trend":
                # Resample annually to show a clear trend
                timeseries = subset.mean(dim=["latitude", "longitude"]).resample(time="YE").mean()
                start_val = float(timeseries.isel(time=0).to_array().mean())
                end_val = float(timeseries.isel(time=-1).to_array().mean())
                diff = end_val - start_val
                direction = "increased" if diff > 0 else "decreased"
                text_response += f"The trend indicates it has {direction} by {abs(diff):.2f} units over this period."
            else:
                timeseries = subset.mean(dim=["latitude", "longitude"])
                
            # Prepare data for plotting in Streamlit/Plotly
            chart_data["times"] = [str(t.values)[:10] for t in timeseries.time]
            
            # Extract first requested variable
            main_var = var_keys[0]
            chart_data["values"] = [float(v) for v in timeseries[main_var].values]
            
        except Exception as e:
            print(f"Error computing stats: {e}")
            return {}, f"Error processing data: {e}"
            
        return chart_data, text_response
