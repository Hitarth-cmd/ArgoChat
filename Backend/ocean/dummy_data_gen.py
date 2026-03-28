import numpy as np
import pandas as pd
import xarray as xr
from pathlib import Path

def generate_dummy_ocean_data():
    """Generates a dummy NetCDF file with temperature and salinity data."""
    print("Generating dummy ocean data...")
    
    # Define dimensions
    # Time: Monthly from 2010 to 2025
    times = pd.date_range("2010-01-01", "2025-12-31", freq="ME")
    # Indian Ocean approximate bounding box (Lat: -40 to 30, Lon: 30 to 110)
    lats = np.linspace(-40, 30, 71) # 1 degree resolution
    lons = np.linspace(30, 110, 81)
    
    # Generate some realistic-looking data with seasonal and long-term trends
    time_idx = np.arange(len(times))
    
    # Temperature: Base 25C + seasonal (sine wave) + slow warming trend + noise
    # Salinity: Base 35 PSU + noise
    n_t, n_lat, n_lon = len(times), len(lats), len(lons)
    
    # Broadcast time explicitly for vectorization
    time_3d = time_idx[:, np.newaxis, np.newaxis]
    lat_3d = lats[np.newaxis, :, np.newaxis]
    
    # Warming trend: ~1 degree over 15 years
    warming = (time_3d / max(1, len(times) - 1)) * 1.0 
    
    # Seasonal cycle based on latitude (opposing phases in N/S hemispheres)
    # North: peak temp in July/Aug. South: peak temp in Jan/Feb
    seasonal = 3.0 * np.sin(2 * np.pi * time_3d / 12 - np.pi/2) * np.sign(lat_3d + 1e-5)
    
    # Base temp varies with latitude (warmer at equator)
    base_temp = 28.0 - 0.2 * np.abs(lat_3d)
    
    temp = base_temp + seasonal + warming + np.random.normal(0, 0.5, (n_t, n_lat, n_lon))
    salinity = 35.0 + np.random.normal(0, 0.2, (n_t, n_lat, n_lon))
    
    ds = xr.Dataset(
        data_vars={
            "temperature": (["time", "latitude", "longitude"], temp, {"units": "Celsius"}),
            "salinity": (["time", "latitude", "longitude"], salinity, {"units": "PSU"}),
        },
        coords={
            "longitude": (["longitude"], lons, {"units": "degrees_east"}),
            "latitude": (["latitude"], lats, {"units": "degrees_north"}),
            "time": times,
        },
        attrs={"description": "Dummy Indian Ocean Data (2010-2025)"}
    )
    
    output_dir = Path(__file__).parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "ocean_data.nc"
    
    ds.to_netcdf(out_path)
    print(f"✅ Dummy data saved to: {out_path}")

if __name__ == "__main__":
    generate_dummy_ocean_data()
