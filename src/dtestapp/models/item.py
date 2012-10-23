from django.db import models


class Item(models.Model):
    class Meta:
        app_label = "dtestapp"
        
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)

    
    @classmethod
    def create(cls, name, descript):
        return Item.objects.create(name=name, description=descript)

    def getName(self):
        return self.name

    def getDescript(self):
        return self.description
