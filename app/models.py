from mongoengine import Document, StringField, ListField, FloatField

class Product(Document):
    category = StringField()
    product_id = StringField()
    title = StringField()
    img = StringField()

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

class Profile(Document):
    product_id = StringField()
    probs = ListField(FloatField())