import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
import requests

nltk.download('punkt') # if necessary...

with open('text_files/turing.txt', 'r') as file:
    turing = file.read().replace('\n', '')

with open('text_files/haley.txt', 'r') as file:
    hopper = file.read().replace('\n', '')

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)


def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))


def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

def get_wikipedia_paragraph(entity):
    r = requests.get("https://en.wikipedia.org/api/rest_v1/page/summary/" + entity.replace(" ", "_"))
    page = r.json()
    return page["extract"]

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')
print(cosine_sim(get_wikipedia_paragraph("Alan Turing"),get_wikipedia_paragraph("Ada Lovelace")))
# print(cosine_sim('a little bird', 'a little bird chirps'))
# print(cosine_sim('a little bird', 'a big dog barks'))



# def get_similarity(paragraph1, paragraph2):
#     stemmer = nltk.stem.porter.PorterStemmer()
#     remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
#     vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')
#     return cosine_sim(paragraph1, paragraph2)
#
# def compute_relevance(main_entity, suggestion):
#     entity_paragraph = get_wikipedia_paragraph(main_entity)
#     suggestion_paragraph = get_wikipedia_paragraph(suggestion)
#     score = get_similarity(entity_paragraph, suggestion_paragraph)
#     return score
#
# print(compute_relevance("Alan Turing", "Grace Hopper"))
