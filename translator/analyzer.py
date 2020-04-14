from .aws_utils import get_text_analysis


def analyse(text, language):
    """
    Analyse a string of text an get a word by word breakdown of the
    text and a tag that describes each word, for example, if a word
    is verb, noun, pronoun, punctuation, etc
    """
    response = get_text_analysis(text, language.short_code)

    sentence_breakdown = []

    for item in response:
        sentence_breakdown.append({
            "word": item["Text"],
            "tag": item["PartOfSpeech"]["Tag"].lower()
        })
    
    return sentence_breakdown