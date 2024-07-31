import re


def has_money(text):
    pattern = re.compile(
        r'^(\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?)|'  # Exemplo: $1,000,000.00
        r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*dollars?)|'  # Exemplo: 1,000,000.00 dollars
        r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*USD)$'  # Exemplo: 1,000,000.00 USD
    )

    return bool(pattern.fullmatch(text))
