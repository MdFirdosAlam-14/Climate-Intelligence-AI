import streamlit as st
from groq import Groq
import crops


MODEL = "openai/gpt-oss-120b"


def build_climate_context(place, current, forecast, hist):
    """Prepare actual application data for the AI assistant."""

    temp = current.get("temperature_2m")
    humidity = current.get("relative_humidity_2m")
    wind = current.get("wind_speed_10m")
    pressure = current.get("surface_pressure")
    precipitation = current.get("precipitation")

    rain7 = float(forecast["rain"].sum())

    context = f"""
LOCATION: {place}

LIVE WEATHER:
Temperature: {temp} °C
Humidity: {humidity} %
Wind speed: {wind} km/h
Surface pressure: {pressure} hPa
Current precipitation: {precipitation} mm

7-DAY FORECAST:
Total forecast rainfall: {rain7:.1f} mm
Forecast details:
{forecast.to_string(index=False)}

HISTORICAL CLIMATE:
Average temperature: {hist["tmean"].mean():.1f} °C
Total historical rainfall: {hist["rain"].sum():.1f} mm
Average wind speed: {hist["wind"].mean():.1f} km/h
Historical records: {len(hist)}

SOIL MOISTURE:
Actual soil moisture sensor/API data is not connected.
Do not invent soil moisture readings.
"""

    # Existing crop recommendation engine
    if temp is not None and humidity is not None:
        recommendations = crops.recommend(
            float(temp),
            float(humidity),
            rain7
        )

        context += "\nCROP SUITABILITY RECOMMENDATIONS:\n"

        for crop in recommendations[:10]:
            context += (
                f"- {crop['Crop']}: "
                f"{crop['Suitability']}% suitability. "
                f"{crop['Reason']}\n"
            )

    return context


def get_ai_response(question, chat_history, climate_context):

    api_key = st.secrets.get("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "Groq API key missing. Check .streamlit/secrets.toml"
        )

    client = Groq(api_key=api_key)

    system_prompt = f"""
You are the AI Climate Assistant inside a Secure Climate
Intelligence Platform.

Your job is to help users with:
- Weather and climate
- Rainfall and temperature
- Agriculture and crop selection
- Crop suitability
- Irrigation guidance
- Soil moisture concepts
- Climate trends

CURRENT APPLICATION DATA:
{climate_context}

IMPORTANT RULES:
1. Use the supplied application data whenever relevant.
2. Never invent weather readings, rainfall measurements,
   soil moisture values or crop observations.
3. Clearly distinguish live weather, forecasts and historical data.
4. If soil moisture data is unavailable, explain that it is not
   currently connected.
5. Crop suitability scores are heuristic estimates, not guarantees.
6. Consider local soil, irrigation, crop variety and season.
7. Do not give dangerous pesticide or chemical instructions.
8. Explain answers in simple language.
9. Reply in the language used by the user:
   Hindi, Hinglish or English.
10. If the user asks an unrelated question, politely explain
    that you are primarily a Climate and Agriculture Assistant.
"""

    messages = [
        {"role": "system", "content": system_prompt}
    ]

    # Keep recent conversation for context
    messages.extend(chat_history[-10:])

    messages.append({
        "role": "user",
        "content": question
    })

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.5,
        max_completion_tokens=1200
    )

    return response.choices[0].message.content