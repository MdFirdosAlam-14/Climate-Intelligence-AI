import requests, pandas as pd, streamlit as st
G = "https://geocoding-api.open-meteo.com/v1/search"
A = "https://archive-api.open-meteo.com/v1/archive"
F = "https://api.open-meteo.com/v1/forecast"
Q = "https://air-quality-api.open-meteo.com/v1/air-quality"

@st.cache_data(ttl=3600)
def coords(city):
    r = requests.get(G, params={"name": city, "count": 1}, timeout=20).json()["results"][0]
    return r["latitude"], r["longitude"], r["name"]

@st.cache_data(ttl=3600)
def history(lat, lon, start, end):
    p = {"latitude": lat, "longitude": lon, "start_date": start, "end_date": end, "timezone": "auto",
         "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,wind_speed_10m_max"}
    df = pd.DataFrame(requests.get(A, params=p, timeout=90).json()["daily"])
    df.columns = ["time", "tmax", "tmin", "tmean", "rain", "wind"]
    df["time"] = pd.to_datetime(df["time"])
    return df.dropna().reset_index(drop=True)

@st.cache_data(ttl=600)
def live(lat, lon):
    p = {"latitude": lat, "longitude": lon, "timezone": "auto", "forecast_days": 7,
         "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,surface_pressure,precipitation",
         "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum"}
    j = requests.get(F, params=p, timeout=20).json()
    d = pd.DataFrame(j["daily"]); d.columns = ["time", "tmax", "tmin", "rain"]
    return j["current"], d

@st.cache_data(ttl=600)
def aqi(lat, lon):
    j = requests.get(Q, params={"latitude": lat, "longitude": lon, "current": "us_aqi,pm2_5,pm10"}, timeout=20).json()
    return j["current"]

@st.cache_data(ttl=3600)
def reverse_coords(lat, lon):
    """Resolve GPS coordinates to a readable place name using Open-Meteo."""
    j = requests.get("https://geocoding-api.open-meteo.com/v1/reverse", params={"latitude":lat,"longitude":lon,"language":"en","format":"json"}, timeout=20).json()
    results = j.get("results", [])
    if results:
        r=results[0]
        return ", ".join(x for x in [r.get("name"),r.get("admin1"),r.get("country")] if x)
    return f"GPS location ({lat:.3f}, {lon:.3f})"
