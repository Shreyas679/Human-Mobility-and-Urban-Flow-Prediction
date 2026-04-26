def get_season_factor(month):
    if month in [10, 11, 12]:
        return 1.4
    elif month in [1, 2, 3]:
        return 1.2
    elif month in [6, 7, 8]:
        return 0.7
    else:
        return 1.0