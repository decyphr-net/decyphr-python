import spacy

nlp = spacy.load("pt_core_news_sm")


def analyse(text):
    """
    Analyse a string of text an get a word by word breakdown of the
    text and a tag that describes each word, for example, if a word
    is verb, noun, pronoun, punctuation, etc
    """
    doc = nlp(text)

    sentence_breakdown = []

    string = ""
    
    for token in doc:
        string += spacy.explain(token.pos_) + " "
        sentence_breakdown.append({
            "word": token.text,
            "tag": spacy.explain(token.pos_)
        })
    return sentence_breakdown