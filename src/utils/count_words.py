import re
import string


def count_words(phrase):
    phrase = phrase.replace("’", "")
    translator = str.maketrans('', '', string.punctuation)
    clean_phrase = phrase.translate(translator)

    pattern = re.compile(r"\b[\w'-]+\b")

    words = pattern.findall(clean_phrase)
    count = len(words)
    return count
