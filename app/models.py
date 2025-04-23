from mongoengine import Document, StringField, IntField

class Review(Document):
    product_id = StringField()
    review = StringField()
    time = StringField()
    nickname = StringField()

class Taghistory(Document):
    comment = StringField()
    tfidf = StringField()
    lda = StringField()
    textrank = StringField()
    llm_wo = StringField()
    llm_w = StringField()
    time = StringField()