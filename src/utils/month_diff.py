def month_diff(d1, d2):

    year_diff = d2.year - d1.year
    month_diff = d2.month - d1.month
    total_month_diff = year_diff * 12 + month_diff

    if d2.day < d1.day:
        total_month_diff -= 1

    return total_month_diff


