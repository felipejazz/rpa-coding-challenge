import re


def has_money(text):
    pattern = re.compile(
        r'^(\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?)|' 
        r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*dollars?)|'  
        r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*USD)$'
    )

    return bool(pattern.fullmatch(text))
