import pytest
from freezegun import freeze_time
from src.utils.is_within_range import is_within_range


@freeze_time("2024-08-01")
@pytest.mark.parametrize("date_str, month_range, expected", [
    ("Aug. 01, 2024", 0, True),  # Mês atual
    ("July 31, 2024", 0, True),  # Mês atual
    ("July 01, 2024", 1, True),  # Mês anterior (Julho)
    ("June 30, 2024", 1, True),  # Mês anterior (Junho)
    ("June 01, 2024", 2, True),  # Mês atual e mês anterior (Junho e Julho)
    ("May 31, 2024", 2, True),  # Dois meses anteriores (Maio e Junho)
    ("May 01, 2024", 3, True),  # Mês atual e dois meses anteriores (Maio, Junho e Julho)
    ("April. 30, 2024", 3, False),  # Três meses anteriores (Abril, Maio, Junho e Julho)
    ("Mar. 31, 2024", 3, False),  # Quatro meses anteriores (Março fora do intervalo)
    ("invalid-date", 3, False)  # Data inválida
])
def test_is_within_range(date_str, month_range, expected):
    assert is_within_range(date_str, month_range) == expected
