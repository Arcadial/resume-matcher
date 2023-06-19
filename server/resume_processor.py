# Import required dependencies
import pandas as pd
import spacy
import nltk
import re

nltk.download("stopwords")
nltk.download("punkt")
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

# Load in predefined en_core_web_sm NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except ImportError:
    print(
        "Spacy's English Language Modules aren't present \n Install them by doing \n python -m spacy download en_core_web_sm"
    )

# Define english stopwords
stop_words = stopwords.words("english")


def base_clean(text):
    def remove_stopwords(
        text, stopwords=stop_words, optional_params=False, optional_words=[]
    ):
        if optional_params:
            stopwords.append([a for a in optional_words])
        return [word for word in text if word not in stopwords]

    def tokenize(text):
        # Removes any useless punctuations from the text
        text = re.sub(r"[^\w\s]", "", text)
        return word_tokenize(text)

    def lemmatize(text):
        """
        Reducing words to their base forms
        For example, for words such as "walks," "walking," and "walked" are reduced to base form "walk"
        A list is taken as an input
        """
        str_text = nlp(" ".join(text))
        lemmatized_text = []
        for word in str_text:
            lemmatized_text.append(word.lemma_)
        return lemmatized_text

    def remove_tags(text, postags=["PROPN", "NOUN", "ADJ", "VERB", "ADV"]):
        """
        Takes in Tags which are allowed by the user and then elimnates the rest of the words
        based on their Part of Speech (POS) Tags.
        """
        filtered = []
        str_text = nlp(" ".join(text))
        for token in str_text:
            if token.pos_ in postags:
                filtered.append(token.text)
        return filtered

    text = tokenize(text)
    text = remove_stopwords(text)
    text = remove_tags(text)
    text = lemmatize(text)
    return text


def reduce_redundancy(text):
    """
    Takes in text that has been cleaned by the _base_clean and uses set to reduce the repeating words
    giving only a single word that is needed.
    """
    return list(set(text))


def get_target_words(text):
    """
    Takes in text and uses Spacy Tags on it, to extract the relevant Noun, Proper Noun words that contain words related to tech and JD.
    """
    target = []
    sent = " ".join(text)
    doc = nlp(sent)
    for token in doc:
        if token.tag_ in ["NN", "NNP"]:
            target.append(token.text)
    return target


def preprocessing(text):
    """
    Returns a nested list, first element containing cleaned data, second element the reduced data, third element relevant Noun, Proper Noun words containing words related to tech and JD.
    """
    sentence = []
    cleaned_sentence = base_clean(text)
    sentence.append(cleaned_sentence)

    reduced_sentence = reduce_redundancy(cleaned_sentence)
    sentence.append(reduced_sentence)

    targetted_sentence = get_target_words(reduced_sentence)
    sentence.append(targetted_sentence)
    return sentence


def do_tfidf(token):
    """
    Takes in text and uses Spacy Tags on it, to extract the relevant Noun, Proper Noun words that contain words related to tech and JD.
    """
    tfidf = TfidfVectorizer(max_df=0.05, min_df=0.002)
    words = tfidf.fit_transform(token)
    sentence = " ".join(tfidf.get_feature_names_out())
    return sentence


def process_resume(resume_raw_txt):
    """Processes resume in text form through description preprocessing and tfidf.

    Parameters (str)
    ----------
    Returns
    -------
    resume_output : pandas dataframe
    """
    # Perform preprocessing
    temp_resume_preprocessing_output = preprocessing(resume_raw_txt)

    # Place format raw and preprocessed data for dataframe creation
    data = {
        "context": resume_raw_txt,
        "cleaned": [temp_resume_preprocessing_output[0]],
        "selective": [temp_resume_preprocessing_output[1]],
        "selective_reduced": [temp_resume_preprocessing_output[2]],
    }
    resume_output = pd.DataFrame(data)

    # Perform TF-IDF
    resume_output["tf_based"] = do_tfidf(temp_resume_preprocessing_output[2])

    return resume_output
