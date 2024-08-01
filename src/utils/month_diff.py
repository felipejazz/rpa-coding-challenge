def month_diff(d1, d2):
    """Calcula a diferença em meses entre duas datas, considerando os dias."""
    # Calcula a diferença em anos e meses
    year_diff = d2.year - d1.year
    month_diff = d2.month - d1.month
    # Calcula a diferença total em meses
    total_month_diff = year_diff * 12 + month_diff

    # Verifica se o dia da data final é anterior ao dia da data inicial
    if d2.day < d1.day:
        total_month_diff -= 1

    return total_month_diff


