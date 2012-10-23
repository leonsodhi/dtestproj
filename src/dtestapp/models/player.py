from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from item import Item
from map import Room
#import dtestapp.engine.game


class Player(models.Model):
    #Map to standard user
    user = models.OneToOneField(User)
   
    class Meta:
        app_label = "dtestapp"

     # Other fields here    
    inventory = models.ManyToManyField(Item)
    dead = models.BooleanField()    
    currLocation = models.ForeignKey(
        'Room',
        null=True,
        blank=True,
        default = None,
        related_name='+',
        on_delete=models.SET_NULL,
    )
    
    @classmethod
    def create(cls, user):
        return Player.objects.create(user = user, dead = False)

    def getDead(self):
        return bool(self.dead)

    def setDead(self, d):
        self.dead = d
        self.save()

    def getLocation(self):
        room = Room.objects.filter(player=self, pk=self.currLocation.pk).select_subclasses()[0]
        room.player = self
        return room

    def hasVisitedBefore(self, locationName):
        return Room.objects.filter(player=self).filter(name__iexact=locationName).exists()

    def setLocation(self, locationName):
        if not self.hasVisitedBefore(locationName):
            raise ValueError("%s doesn't exist" % locationName)

        self.currLocation = Room.objects.filter(player=self).filter(name__iexact=locationName).select_subclasses()[0]
        self.save()                        
        
    def addToInventory(self, item):
        self.inventory.add(item)

    def delFromInventory(self, item):
        self.inventory.remove(item)

    def getInventoryNames(self):
        names = []
        for i in list(self.inventory.all()):
            names.append(i.getName())
        return names
        
    def inventoryContains(self, itemName):
        return self.inventory.filter(name__iexact=itemName).exists()
        

#def createPlayer(sender, instance, created, **kwargs):    
#    if created:
#        pl = Player.create(instance)
        #dtestapp.engine.game.initPlayer(pl)
        #Player.objects.create(user=instance)
#post_save.connect(createPlayer, sender=User, dispatch_uid="users-profilecreation-signal")
