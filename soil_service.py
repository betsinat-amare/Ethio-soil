import requests

def fetch_soilgrids_properties(lat: float, lon: float) -> dict:
    """
    Queries the ISRIC SoilGrids v2.0 REST API for a given latitude and longitude 
    to retrieve real soil pH and organic carbon content.
    """
    # SoilGrids properties: phh2o (pH in water) and ocd (organic carbon density)
    url = f"https://rest.isric.org/soilgrids/v2.0/properties/query"
    
    params = {
        "lat": lat,
        "lon": lon,
        "property": ["phh2o", "ocd"],
        "depth": "0-5cm", # Surface soil layer
        "value": "mean"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            layers = data.get("properties", {}).get("layers", [])
            
            soil_results = {}
            for layer in layers:
                name = layer.get("name")
                # Extract the mean value for the 0-5cm depth layer
                depths = layer.get("depths", [])
                if depths:
                    mean_val = depths[0].get("values", {}).get("mean")
                    # SoilGrids often multiplies pH and values by scaling factors (e.g., pH is stored * 10)
                    if name == "phh2o" and mean_val is not None:
                        soil_results["soil_ph"] = mean_val / 10.0
                    elif name == "ocd" and mean_val is not None:
                        soil_results["organic_carbon"] = mean_val / 10.0
            
            return {
                "success": True,
                "source": "SoilGrids API (ISRIC)",
                "data": soil_results
            }
        else:
            return {
                "success": False,
                "error": f"SoilGrids API returned status code {response.status_code}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }