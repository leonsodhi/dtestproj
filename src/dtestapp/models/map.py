from django.db import models
from model_utils.managers import InheritanceManager

import fields
from dtestapp.engine.err import ErrorType
import dtestapp.engine.util
from item import Item


class Room(models.Model):
    NAME = ""    
        
    objects = InheritanceManager()

    class Meta:
        app_label = "dtestapp"
    
    name = models.CharField(max_length=255)
    description = models.TextField() 
    player = models.ForeignKey(
        'Player',
        default = None,
        related_name='+',        
    )
    roomContents = models.ManyToManyField(Item)


    def _setupRoom(self):
        pass

    
    @classmethod
    def create(cls, player):
        #TODO: name should be an int identifier of some kind rather than a string
        obj = cls.objects.create(name = cls.NAME, description = cls.DEFAULT_DESCRIPTION, player=player)
        obj._setupRoom()        
        return obj


    @classmethod
    def getName(cls):
        return cls.NAME
    
    def getDescription(self):        
        return self.description         
    
    def _goToRoom(self, roomClass):
        if not self.player.hasVisitedBefore(roomClass.getName()):
            room = roomClass.create(self.player)
        self.player.setLocation(roomClass.getName())

        return self.player.getLocation().getDescription()


    def getRoomContentsLabels(self):
        labels = []
        for i in list(self.roomContents.all()):        
            labels.append(i.getName())
        return labels


    def _itemInRoom(self, itemName):
        return self.roomContents.filter(name__iexact=itemName).exists()


    def _use(self, b):
        return ("", None, None)
    def use(self, b):
        if not self._itemInRoom(b):
            return (None, "%s doesn't exist in the room" % b, ErrorType.GAME)
        
        (txt, err, errType) = self._use(b)
        if txt == "" and err == None and errType == None:
            return ("I can't do anything with that", None, None)
        return (txt, err, errType)


    def _useWith(self, a, b):
        return ("", None, None)         
    def useWith(self, a, b):
        if not self.player.inventoryContains(a):
            return (None, "You don't have %s" % a, ErrorType.GAME)
        if not self._itemInRoom(b):
            return (None, "%s doesn't exist in the room" % b, ErrorType.GAME)
                
        (txt, err, errType) = self._useWith(a, b)
        if txt == "" and err == None and errType == None:
            return ("I can't use those two things together", None, None)
        return (txt, err, errType)


    def _talk(self, thing):
        return ("", None, None)
    def talk(self, thing):              
        if not self._itemInRoom(thing):
            return (None, "%s doesn't exist" % thing, ErrorType.GAME)
        (txt, err, errType) = self._talk(thing)
        if txt == "" and err == None and errType == None:
            return ("I can't talk to that", None, None)
        return (txt, err, errType)
     

    def _lookat(self, item):
        return ("", None, None)
    def lookat(self, item):
        if (not self._itemInRoom(item) and
            not self.player.inventoryContains(item)):
                return (None, "%s doesn't exist anywhere" % item, ErrorType.GAME)

        (txt, err, errType) = self._lookat(item)
        if txt == "" and err == None and errType == None:
            itemDescript = Item.objects.get(name__iexact=item).getDescript()
            if itemDescript == "":
                return ("It's a %s" % item, None, None)
            else:
                return (itemDescript, None, None)
        return (txt, err, errType)


    def _pickUp(self, item):
        return ("", None, None)
    def pickUp(self, item):
        if not self._itemInRoom(item):
            return (None, "%s doesn't exist anywhere in the room" % item, ErrorType.GAME)

        (txt, err, errType) = self._pickUp(item)
        if txt == "" and err == None and errType == None:
            return ("I don't want that", None, None)
        return (txt, err, errType)
        


    
class CentralCorridor(Room):
    NAME = "Central Corridor"
    DEFAULT_DESCRIPTION = """
The Gothons of Planet Percal #25 have invaded your ship and destroyed
your entire crew.  You are the last surviving member and your last
mission is to get the neutron destruct bomb from the Weapons Armory,
put it in the bridge, and blow the ship up after getting into an 
escape pod.

You're running down the central corridor to the Weapons Armory when
a Gothon jumps out, red scaly skin, dark grimy teeth, and evil clown costume
flowing around his hate filled body.  He's blocking the door to the
Armory and about to pull a weapon to blast you.
            """
            
    class Meta:
        app_label = "dtestapp"

    def _setupRoom(self):
        self.roomContents.add(dtestapp.engine.util.getItem("gothon"))
        self.roomContents.add(dtestapp.engine.util.getItem("LaserWeaponArmoryExit"))          
        
    def _use(self, b):
        """Return: (txt, err, errType)"""                   

        txt = ""
        if dtestapp.engine.util.stricmp(b,"LaserWeaponArmoryExit"):
            if not self._itemInRoom("gothon"):
                newRoomDescript = self._goToRoom(LaserWeaponArmory)                
                txt = newRoomDescript
            else:
                self.player.setDead(True)
                txt = """
Like a world class boxer you dodge, weave, slip and slide
your way to the door right
as the Gothon's blaster cranks a laser past your head.
In the middle of your artful dodge your foot slips and you
bang your head on the metal wall and pass out.
You wake up shortly after only to die as the Gothon stomps on
your head and eats you.
                    """                    
        return (txt, None, None)


    def _useWith(self, a, b):        
        """Return: (txt, err, errType)"""       
        
        txt = ""
        if dtestapp.engine.util.stricmp(a,"blaster") and dtestapp.engine.util.stricmp(b,"gothon"):
            self.player.setDead(True)
            txt = """
Quick on the draw you yank out your blaster and fire it at the Gothon.
His clown costume is flowing and moving around his body, which throws
off your aim.  Your laser hits his costume but misses him entirely.  This
completely ruins his brand new costume his mother bought him, which
makes him fly into an insane rage and blast you repeatedly in the face until
you are dead.  Then he eats you.
                """               

        return (txt, None, None)


    def _talk(self, thing):           
        """Return: (txt, err, errType)"""
      
        txt = ""
        if dtestapp.engine.util.stricmp(thing,"gothon"):
            self.roomContents.remove(dtestapp.engine.util.getItem("gothon"))
            self.roomContents.add(dtestapp.engine.util.getItem("paper"))
            self.roomContents.add(dtestapp.engine.util.getItem("deadgothon"))

            self.description = """
The Gothons of Planet Percal #25 have invaded your ship and destroyed
your entire crew.  You are the last surviving member and your last
mission is to get the neutron destruct bomb from the Weapons Armory,
put it in the bridge, and blow the ship up after getting into an 
escape pod.
                """
            self.save()
                            
            txt = """
Lucky for you they made you learn Gothon insults in the academy.
You tell the one Gothon joke you know:
Lbhe zbgure vf fb sng, jura fur fvgf nebhaq gur ubhfr, fur fvgf nebhaq gur ubhfr.
The Gothon stops, tries not to laugh, then busts out laughing and can't move.
While he's laughing you run up and shoot him square in the head
putting him down. As he falls to the ground, you notice a piece of paper 
floating to the floor.
                """
        return (txt, None, None)


    def _pickUp(self, item):       
        txt = ""
        if dtestapp.engine.util.stricmp(item,"paper"):
            paper = dtestapp.engine.util.getItem("paper")
            self.roomContents.remove(paper)
            self.player.addToInventory(paper)            
            txt = "Picked up %s" % paper.getName()                    
        
        return (txt, None, None)


class LaserWeaponArmory(Room):
    NAME = "Laser Weapon Armory"
    DEFAULT_DESCRIPTION = """
You do a dive roll into the Weapon Armory, crouch and scan the room
for more Gothons that might be hiding.  It's dead quiet, too quiet.
You stand up and run to the far side of the room and find the
neutron bomb in its container.  There's a keypad lock on the box
and you need the code to get the bomb out.  If you get the code
wrong 4 times then the lock closes forever. The code is 3 digits.
                        """ 
    class Meta:
        app_label = "dtestapp"

    def _setupRoom(self):
        self.roomContents.add(dtestapp.engine.util.getItem("CentralCorridorExit"))
        self.roomContents.add(dtestapp.engine.util.getItem("TheBridgeExit")) 
        self.roomContents.add(dtestapp.engine.util.getItem("NeutronBombContainer"))          
        
    def _use(self, b):
        """Return: (txt, err, errType)"""        
                    
        txt = ""
        if dtestapp.engine.util.stricmp(b, "CentralCorridorExit"):
    	    newRoomDescript = self._goToRoom(CentralCorridor)        
            txt = newRoomDescript

        if dtestapp.engine.util.stricmp(b, "NeutronBombContainer"):
            newRoomDescript = self._goToRoom(NeutronBombContainer)
            txt = newRoomDescript

        if dtestapp.engine.util.stricmp(b, "TheBridgeExit"):
            if self.player.inventoryContains("neutronbomb"):
                newRoomDescript = self._goToRoom(TheBridge)        
                txt = newRoomDescript                
            else:
                txt = "I've got to get the neutron bomb before I go to the bridge"

        return (txt, None, None)


    def _pickUp(self, item):        
        txt = ""
            
        if dtestapp.engine.util.stricmp(item, "NeutronBombContainer"):        
            txt = "I can't it's bolted to the ground and even if I could it's of no use to me sealed"

        return (txt, None, None)


class NeutronBombContainer(Room):
    NAME = "Neutron Bomb Container"
    DEFAULT_DESCRIPTION = "DYNAMIC"

    MAXATTEMPTS = 3
    
    class Meta:
        app_label = "dtestapp"           
    
    _containerCode = [4,7,2] #TODO: this should be set externally to match up with the paper
    
    currAttemptDigits = fields.IntegerListField()
    failedAttempts = models.IntegerField(default = 0)
    containerOpen = models.BooleanField(default = False)
    
        
    def _setupRoom(self):
        self.roomContents.add(dtestapp.engine.util.getItem("LaserWeaponArmoryExit"))
        self.roomContents.add(dtestapp.engine.util.getItem("NeutronBomb"))
        for i in range(10):
            self.roomContents.add(dtestapp.engine.util.getItem(str(i)))
        self.roomContents.add(dtestapp.engine.util.getItem("enter"))


    def getDescription(self):
        self.description = """
You stare at the container control panel, it appears to be
a standard numeric keypad with buttons labelled 0 to 9 with
an enter key at the bottom.
                    """                            
        if not self.player.inventoryContains("paper"):
            self.description += """
With the knowledge that 3 wrong
attempts will seal the bomb forever, you attempt to guess the
code.
                    """
        self.save()     
        return self.description    
        
    
    def _use(self, b):
        """Return: (txt, err, errType)"""        
                    
        txt = ""        
        
        try:
            num = int(b)
            if num >= 0 and num <= 9:
                if len(self.currAttemptDigits) == 3:
                    self.currAttemptDigits = []                
                self.currAttemptDigits.append(num)
                self.save()                
                txt = str(self.currAttemptDigits).strip('[').strip(']')                
                return (txt, None, None)              
        except:
            pass
            
        if dtestapp.engine.util.stricmp(b, "LaserWeaponArmoryExit"):
            self.currAttemptDigits = []
            self.save()
    	    newRoomDescript = self._goToRoom(LaserWeaponArmory)        
            txt = newRoomDescript
            return (txt, None, None)    
        if dtestapp.engine.util.stricmp(b, "Enter"):
            if self.containerOpen:
                txt = "The container is already open"
                return (txt, None, None)
            if len(self.currAttemptDigits) != len(self._containerCode):
                txt = "Not enough digits, so far you've got: %s" % str(self.currAttemptDigits).strip('[').strip(']')
                return (txt, None, None)
            if self.currAttemptDigits == self._containerCode:
                self.containerOpen = True
                self.save()
                txt = "The container clicks open and the seal breaks letting gas out"                    
                return (txt, None, None)
            else:
                self.failedAttempts += 1
                self.save()
                if self.failedAttempts == self.MAXATTEMPTS:
                    self.player.setDead(True)
                    txt = """
The lock buzzes one last time and then you hear a sickening
melting sound as the mechanism is fused together.
You decide to sit there, and finally the Gothons blow up the
ship from their ship and you die.
                            """
                    return (txt, None, None)
                else:
                    txt = "The container doesn't budge, the code must have been wrong, only %s attempts left" % (self.MAXATTEMPTS - self.failedAttempts)
                    return (txt, None, None)
       
                    
        return (txt, None, None)


    def _pickUp(self, item):        
        txt = ""
            
        if dtestapp.engine.util.stricmp(item, "NeutronBomb"):
            if self.containerOpen:       
                neutronBomb = dtestapp.engine.util.getItem("NeutronBomb")         
                self.roomContents.remove(neutronBomb)
                self.player.addToInventory(neutronBomb)       
                txt = "Picked up %s" % item
            else:
                txt = "You can't get to the bomb whilst the container is sealed"
        
        return (txt, None, None)


class TheBridge(Room):
    NAME = "The Bridge"
    DEFAULT_DESCRIPTION = """
You burst onto the Bridge with the netron destruct bomb
under your arm and surprise 5 Gothons who are trying to
take control of the ship.  Each of them has an even uglier
clown costume than the last.  They haven't pulled their
weapons out yet, as they see the active bomb under your
arm and don't want to set it off.
            """

    class Meta:
        app_label = "dtestapp"

    def _setupRoom(self):
        self.roomContents.add(dtestapp.engine.util.getItem("GothonGroup"))
        self.roomContents.add(dtestapp.engine.util.getItem("BridgeFloor"))
        self.roomContents.add(dtestapp.engine.util.getItem("EscapePodsExit"))                                        

    def _use(self, b):
        txt = ""

        if dtestapp.engine.util.stricmp(b, "EscapePodsExit"):
            if self.player.inventoryContains("neutronbomb"):
                txt = "I can't leave with an armed neutron bomb under my arm!"                                
            else:
                newRoomDescript = self._goToRoom(EscapePods)        
                txt = newRoomDescript
                
        return (txt, None, None)
        
                
    def _useWith(self, a, b):        
        """Return: (txt, err, errType)"""       
        
        txt = ""
        if dtestapp.engine.util.stricmp(a, "neutronbomb") and dtestapp.engine.util.stricmp(b, "gothongroup"):
            self.player.setDead(True)
            txt = """
In a panic you throw the bomb at the group of Gothons
and make a leap for the door.  Right as you drop it a
Gothon shoots you right in the back killing you.
As you die you see another Gothon frantically try to disarm
the bomb. You die knowing they will probably blow up when
it goes off.
                """               

        if dtestapp.engine.util.stricmp(a, "neutronbomb") and dtestapp.engine.util.stricmp(b, "bridgefloor"):
            neutronBomb = dtestapp.engine.util.getItem("NeutronBomb")
            self.player.delFromInventory(neutronBomb)
            self.roomContents.add(neutronBomb)
            txt = """
You gently place the armed neutron bomb on the floor,
the gothons put their hands up and start to sweat
                """
                
        return (txt, None, None)


class EscapePods(Room):
    NAME = "Escape Pods"    
    DEFAULT_DESCRIPTION = """
You leap into the Escape pod chamber, punch the close button 
and blast the lock trapping the gothons in the bridge with the 
bomb.

You now need to pick one of the pods to take, some of them could
be damaged but you don't have time to properly examine them. 
There are 5 pods with various labels on them, which one do you want 
to use?
            """

    class Meta:
        app_label = "dtestapp"
        
    def _setupRoom(self):
        self.roomContents.add(dtestapp.engine.util.getItem("Pod1"))
        self.roomContents.add(dtestapp.engine.util.getItem("Pod2"))
        self.roomContents.add(dtestapp.engine.util.getItem("Pod3"))
        self.roomContents.add(dtestapp.engine.util.getItem("Pod42"))
        self.roomContents.add(dtestapp.engine.util.getItem("Pod5"))

    def _use(self, b):
        """Return: (txt, err, errType)"""        
        
        txt = ""
        if (dtestapp.engine.util.stricmp(b, "Pod1") or 
            dtestapp.engine.util.stricmp(b, "Pod2") or
            dtestapp.engine.util.stricmp(b, "Pod3") or 
            dtestapp.engine.util.stricmp(b, "Pod5")):
            self.player.setDead(True)
            txt = """
You jump into the pod and hit the eject button.
The pod escapes out into the void of space, then
implodes as the hull ruptures, crushing your body
into jam jelly.
            """

        if dtestapp.engine.util.stricmp(b, "Pod42"):
            newRoomDescript = self._goToRoom(TheEnd)
            txt = newRoomDescript

        return (txt, None, None)


class TheEnd(Room):
    NAME = "The End"   
    DEFAULT_DESCRIPTION = """
You jump into the pod and hit the eject button.
It easily slides out into space heading to
the planet below.  As it flies to the planet, you look
back and see your ship implode then explode like a
bright star, taking out the Gothon ship at the same
time. You won!
            """        

    class Meta:
        app_label = "dtestapp"            
