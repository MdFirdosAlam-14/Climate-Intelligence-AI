"""Simple weather/season crop suitability scoring (advisory, not agronomic guarantee)."""
from datetime import date

CROPS = [
    # name, category, seasons(months), min_temp, max_temp, rainfall target mm/month, description
    ("Rice (Paddy)", "Field crop", [6,7,8,9], 20, 35, 180, "Warm conditions and substantial water availability."),
    ("Wheat", "Field crop", [11,12,1,2,3], 10, 25, 60, "Cool growing season; avoid excessive heat during grain filling."),
    ("Maize", "Field crop", [3,4,5,6,7,8], 18, 32, 100, "Warm weather and well-drained soil."),
    ("Mustard", "Field crop", [10,11,12,1,2], 10, 25, 50, "Cool, relatively dry conditions."),
    ("Potato", "Vegetable", [10,11,12,1,2], 10, 25, 60, "Cool conditions and loose, well-drained soil."),
    ("Tomato", "Vegetable", [2,3,4,5,9,10,11], 18, 30, 80, "Moderate temperatures; avoid prolonged heat and waterlogging."),
    ("Onion", "Vegetable", [10,11,12,1,2,3], 12, 30, 60, "Cool early growth and dry conditions during bulb maturity."),
    ("Cabbage", "Vegetable", [10,11,12,1,2], 10, 25, 70, "Cool-season vegetable."),
    ("Cauliflower", "Vegetable", [10,11,12,1,2], 10, 25, 70, "Cool weather; varieties differ by season."),
    ("Spinach", "Vegetable", [10,11,12,1,2], 8, 25, 60, "Cool conditions and steady soil moisture."),
    ("Brinjal (Eggplant)", "Vegetable", [2,3,4,5,6,7,8,9], 20, 32, 100, "Warm conditions and no frost."),
    ("Okra (Ladyfinger)", "Vegetable", [3,4,5,6,7], 22, 35, 100, "Warm conditions; sensitive to cold."),
    ("Cucumber", "Vegetable", [3,4,5,6,7], 20, 32, 100, "Warm conditions and consistent moisture."),
    ("Carrot", "Vegetable", [10,11,12,1], 10, 25, 60, "Cool weather and loose soil."),
    ("Radish", "Vegetable", [10,11,12,1,2], 8, 25, 60, "Cool-season crop with quick maturity."),
    ("Green Peas", "Vegetable", [10,11,12,1], 8, 24, 60, "Cool weather."),
    ("Pumpkin", "Vegetable", [3,4,5,6,7], 20, 32, 100, "Warm season and ample space."),
    ("Bottle Gourd", "Vegetable", [3,4,5,6,7], 20, 32, 100, "Warm season and adequate moisture."),
    ("Bitter Gourd", "Vegetable", [3,4,5,6,7], 20, 32, 100, "Warm weather and well-drained soil."),
    ("Capsicum", "Vegetable", [10,11,12,1,2], 15, 28, 70, "Moderate conditions; protect from temperature extremes."),
    ("Mango", "Fruit", [2,3,4,5,6], 24, 35, 100, "Warm climate; suitability depends strongly on local orchard conditions."),
    ("Banana", "Fruit", [1,2,3,4,5,6,7,8,9,10,11,12], 22, 35, 150, "Warm, humid climate with reliable water."),
    ("Papaya", "Fruit", [2,3,4,5,6,7,8,9], 22, 32, 100, "Warm climate; sensitive to waterlogging and cold."),
    ("Guava", "Fruit", [2,3,4,5,6,7,8,9], 18, 32, 80, "Adaptable fruit tree; consider soil and local variety."),
    ("Watermelon", "Fruit", [3,4,5,6], 22, 32, 80, "Warm season; rainfall during fruiting may affect quality."),
    ("Muskmelon", "Fruit", [3,4,5], 22, 32, 70, "Warm, relatively dry conditions during fruit development."),
    ("Strawberry", "Fruit", [10,11,12,1], 10, 25, 60, "Cool season; needs careful variety and production management."),
    ("Pineapple", "Fruit", [3,4,5,6,7,8], 20, 32, 120, "Warm, humid conditions and well-drained soil."),
    ("Litchi", "Fruit", [2,3,4,5,6], 20, 32, 100, "Subtropical climate; orchard establishment is long-term."),
    ("Lemon", "Fruit", [2,3,4,5,6,7,8,9], 18, 32, 80, "Warm climate; protect from frost and waterlogging."),
]

def recommend(temp, humidity, rain_mm, month=None):
    month = month or date.today().month
    rows=[]
    for name, category, months, lo, hi, rain_target, note in CROPS:
        temp_score = 1 if lo <= temp <= hi else max(0, 1 - min(abs(temp-lo), abs(temp-hi))/15)
        seasonal = 1 if month in months else 0.25
        rain_score = 1 if rain_mm is None else max(0.2, 1-abs(rain_mm-rain_target)/max(rain_target,100))
        score = 0.55*temp_score + 0.30*seasonal + 0.15*rain_score
        rows.append({"Crop":name,"Category":category,"Suitability":round(score*100),"Reason":note})
    return sorted(rows,key=lambda r:r["Suitability"],reverse=True)
