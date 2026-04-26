import pandas as pd
import random

locations = [
    ("Beach", "beach", "tourist"),
    ("City Area", "urban", "urban"),
    ("Hill Station", "tourist", "tourist"),
    ("Office Area", "office", "urban"),
    ("Mall Area", "mall", "urban"),
    ("Market Area", "market", "urban"),
    ("Village Area", "rural", "rural"),
]

def season_factor(month):
    if month in [10,11,12]: return 1.4
    if month in [1,2,3]: return 1.2
    if month in [6,7,8]: return 0.7
    return 1.0

def crowd_logic(loc_type, hour, weekday, month):
    base = 30

    if 17 <= hour <= 20: base += 30
    elif 10 <= hour <= 16: base += 15
    else: base -= 10

    if weekday >= 5: base += 20

    base *= season_factor(month)

    if loc_type == "beach":
        if 16 <= hour <= 18: base += 25
        if 18 <= hour <= 20: base += 20
        if 20 <= hour <= 23: base += 30

    elif loc_type == "office":
        if 9 <= hour <= 11: base += 25
        if 17 <= hour <= 20: base += 30

    elif loc_type == "mall":
        if 17 <= hour <= 21: base += 35

    elif loc_type == "market":
        base += 20

    elif loc_type == "tourist":
        if 16 <= hour <= 18: base += 30

    elif loc_type == "rural":
        base -= 15

    base += random.randint(-5,5)

    return int(max(5, min(100, base)))

data = []

for _ in range(1000):
    loc, loc_type, context = random.choice(locations)

    hour = random.choice([9,11,13,15,17,18,19,20,22])
    weekday = random.randint(0,6)
    month = random.randint(1,12)

    data.append([
        loc, hour, weekday, month,
        1 if weekday>=5 else 0,
        0,
        loc_type, context,
        1 if 16<=hour<=18 else 0,
        1 if loc_type=="beach" and hour>=20 else 0,
        1 if loc_type=="office" and (9<=hour<=11 or 17<=hour<=20) else 0,
        season_factor(month),
        crowd_logic(loc_type, hour, weekday, month)
    ])

df = pd.DataFrame(data, columns=[
    "location_name","hour","weekday","month",
    "is_weekend","is_holiday",
    "location_type","context_type",
    "is_sunset_time","is_nightlife_time","is_office_rush",
    "season_factor","crowd_density"
])

df.to_csv("final_dataset_1000.csv", index=False)
print("Dataset generated at:", "final_dataset_1000.csv")