import asyncio
from Backend.ocean.ocean_processor import OceanProcessor
import sys
import json

async def test():
    op = OceanProcessor()
    print('Testing query: Show the ocean temperature trend from 2015 to 2025 as a line chart for the Indian Ocean.')
    params = await op.extract_query_json('Show the ocean temperature trend from 2015 to 2025 as a line chart for the Indian Ocean.')
    print('EXTRACTED PARAMS:', json.dumps(params, indent=2))
    
    data, text = op.process_data(params)
    print('TEXT RESPONSE:', text)
    print('DATA TIMES LEN:', len(data.get('times', [])))
    if data.get('times'):
        print('FIRST 5 TIMES:', data['times'][:5])
        print('FIRST 5 VALUES:', data['values'][:5])

    print("\n\nChecking dataset directly for 2015-2025...")
    try:
        start_year = "2015"
        end_year = "2025"
        subset = op.ds['temperature'].sel(
            time=slice(f"{start_year}-01-01", f"{end_year}-12-31")
        )
        print('Raw subset times found:', len(subset.time))
    except Exception as e:
        print('Error slicing directly:', e)

if __name__ == "__main__":
    asyncio.run(test())
