from django.db import models
from datetime import datetime
from mongoengine import Document, StringField, IntField,DateTimeField
# Create your models here.

class plantaItem(Document):
    name = StringField(max_length=200, required= True)
    Irrigation = IntField(min_value=1, required= True)
    Size = IntField(min_value=1, required= True)
    Price = IntField(min_value=1, required= True)
    material = StringField(max_length=20)
    creation_date = DateTimeField(default=datetime.now)
    author = StringField(max_length=20)
    
    meta = {
        'collection': "plantas",
        'ordering': ['-creation_date']
    }
    
    def as_dic(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "Irrigation": self.Irrigation,
            "Size": self.Size,
            "Price": self.Price,
            "material": self.material
        }        
    
    def __str__(self):
        return f"{self.name} : {self.Irrigation}x{self.Size}x{self.Price} {self.material}"
    
