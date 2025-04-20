from mongoengine import Document, StringField, IntField

class Review(Document):
    product_id = StringField()
    review = StringField()