def plural_days(n: int) -> str:
    """
    Склонение день/дня/дней
    """
    days = ["день", "дня", "дней"]
    remainder = ["Остался", "Осталось"]

    if n % 10 == 1 and n % 100 != 11:
        p = 0
        s = 0
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        p = 1
        s = 1
    else:
        p = 2
        s = 1

    return f"{remainder[s]} {str(n)} {days[p]}"
