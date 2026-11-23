
import pandas as pd


def assess_irrigation(crop_name, current, forecast, soil_status):
    """
    Rule-based irrigation assessment.

    Uses weather forecast and farmer-reported soil condition.
    Does not claim actual soil moisture or exact water quantity.
    """

    # Current weather
    temp = current.get("temperature_2m")
    humidity = current.get("relative_humidity_2m")

    # Forecast rainfall
    rain_values = pd.to_numeric(
        forecast["rain"], errors="coerce"
    ).fillna(0)

    rain_7d = float(rain_values.sum())
    rain_48h = float(rain_values.head(2).sum())

    forecast_temp = pd.to_numeric(
        forecast["tmax"], errors="coerce"
    ).dropna()

    max_temp = (
        float(forecast_temp.max())
        if not forecast_temp.empty
        else None
    )

    # Normalize farmer's field observation
    soil_status = soil_status.lower().strip()

    priority = "Medium"
    headline = "Check field conditions"
    actions = []
    reasons = []

    # Rainfall assessment
    if rain_48h >= 20:
        reasons.append(
            f"Approximately {rain_48h:.1f} mm rainfall "
            "is forecast in the next 48 hours."
        )
    elif rain_7d < 5:
        reasons.append(
            "Very little rainfall is forecast over the next 7 days."
        )
    else:
        reasons.append(
            f"Forecast rainfall over 7 days is {rain_7d:.1f} mm."
        )

    # Temperature assessment
    if max_temp is not None and max_temp >= 35:
        reasons.append(
            f"High temperature is possible, reaching {max_temp:.1f} °C."
        )

    if temp is not None:
        reasons.append(
            f"Current temperature is {float(temp):.1f} °C."
        )

    if humidity is not None:
        reasons.append(
            f"Current relative humidity is {float(humidity):.0f}%."
        )

    # Decision rules
    if soil_status == "wet":
        priority = "Low"
        headline = "Avoid additional irrigation for now"
        actions.append(
            "Check drainage and avoid waterlogging."
        )
        actions.append(
            "Recheck the soil before the next irrigation."
        )

    elif soil_status == "dry":
        if rain_48h >= 20:
            priority = "Medium"
            headline = "Rain is expected; reassess before irrigating"
            actions.append(
                "Check the field again after the forecast rainfall."
            )
            actions.append(
                "If the crop is visibly stressed, consider "
                "appropriate irrigation rather than waiting blindly."
            )
        else:
            priority = "High"
            headline = "Irrigation may be needed soon"
            actions.append(
                "Inspect the root zone and confirm that the soil is dry."
            )
            actions.append(
                "If the crop needs water, plan irrigation according "
                "to its growth stage and local farming practice."
            )

    elif soil_status == "moist":
        if rain_48h >= 20:
            priority = "Low"
            headline = "Wait and monitor upcoming rainfall"
            actions.append(
                "Avoid unnecessary irrigation before expected rain."
            )
        elif max_temp is not None and max_temp >= 35 and rain_7d < 5:
            priority = "Medium"
            headline = "Monitor the field during hot, dry weather"
            actions.append(
                "Check soil moisture near the crop roots more frequently."
            )
            actions.append(
                "Irrigate only if the soil begins drying or the crop "
                "shows water stress."
            )
        else:
            priority = "Low"
            headline = "No immediate irrigation signal"
            actions.append(
                "Continue monitoring soil and crop condition."
            )

    else:
        priority = "Medium"
        headline = "Soil condition needs to be checked"
        actions.append(
            "Use a soil-by-feel check near the crop root zone."
        )
        actions.append(
            "Do not schedule irrigation using weather data alone."
        )

    # Additional rainfall warning
    if rain_48h >= 20:
        actions.append(
            "Check field drainage because heavy rainfall may cause "
            "waterlogging in poorly drained soil."
        )

    return {
        "crop": crop_name,
        "priority": priority,
        "headline": headline,
        "rain_48h": round(rain_48h, 1),
        "rain_7d": round(rain_7d, 1),
        "max_temp": (
            round(max_temp, 1) if max_temp is not None else None
        ),
        "reasons": reasons,
        "actions": actions,
        "soil_status": soil_status,
        "data_note": (
            "Soil condition is farmer-reported, not sensor-measured. "
            "This is a preliminary advisory, not an exact irrigation "
            "schedule or water-quantity calculation."
        )
    }
