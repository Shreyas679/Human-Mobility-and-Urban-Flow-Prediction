from datetime import datetime

def extract_features(date, time):
    dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

    return (
        dt.hour,
        dt.weekday(),
        dt.month,
        1 if dt.weekday()>=5 else 0,
        0
    )