from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import jieba
import jieba.analyse as analyse

def tfidf(text, top_n=5):
    keywords = analyse.extract_tags(
        text, 
        topK=top_n
    )
    return keywords

def lda(text, top_n=5, n_topics=1):
    words = " ".join(jieba.cut(text))
    corpus = [words]
    vectorizer = CountVectorizer(max_features=1000)
    X = vectorizer.fit_transform(corpus)
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(X)
    feature_names = vectorizer.get_feature_names_out()
    keywords = []
    for topic in lda.components_:
        top_features_ind = topic.argsort()[:-top_n - 1:-1]
        topic_keywords = [feature_names[i] for i in top_features_ind]
        keywords.append(topic_keywords)
    
    if n_topics == 1:
        return keywords[0]
    return keywords

def textrank(text, top_n=5):
    keywords = analyse.textrank(
        text, 
        topK=top_n, 
        withWeight=False, 
        allowPOS=('n', 'vn', 'v', 'a')
    )
    return keywords