import logging
import os
import sys
#inc = os.getcwd()
#sys.path.append(inc)

from dtestapp.models import map
from dtestapp.models.player import Player
#import worldItems
from err import ErrorType
import dtestapp.engine.util
#import util
#from item import Item
#import player


#logging.basicConfig(format="[%(filename)s:%(lineno)s:%(levelname)s] %(message)s", level=logging.DEBUG)


class Cmd(object):
    def __init__(self, name, numParams, descript):
        self.name = name
        self.numParams = numParams
        self.descript = descript
        
#class Game(object):
_cmds = [
        Cmd("room", 0, "Show all objects in the room"),
        Cmd("inven", 0, "Show current inventory"),
        Cmd("use", 1, "Use an object e.g. use a"),
        Cmd("use", 2,  "Use an object on an object in the room e.g. use a b"),
        #Cmd("combine", 2, "combine two objects in the _players inventory"),
        Cmd("pickup", 1, "Pickup an object e.g. pickup a"),
        Cmd("lookat", 1, "Look at a room or inventory object e.g. lookat a"),
        Cmd("talk", 1, "Talk to someone or something e.g. talk a")
    ]
        
    #def __init__(self):               
    #    self._player = testproj.player.Player() #TODO: how to save the contents of rooms?
    #    self._player.setNewLocation(map.CentralCorridor(self._player))
    #    self._player.addToInventory(worldItems.g_ItemDict["blaster"])

    
def getCmdHelp():
    cmdHelp = []
    for c in _cmds:
        t = (c.name, c.descript)
        cmdHelp.append(t)
    return cmdHelp


def createPlayer(user):
    player = Player.create(user)
    
    cc = map.CentralCorridor.create(player)
    player.setLocation(cc.getName())    
    d2 = player.getLocation().getDescription()
                
    blaster = dtestapp.engine.util.getItem("blaster")
    player.addToInventory(blaster)

    return player

            
def _validateCmd(cmdList):
    txtCmd = None
    
    for d in cmdList:
        if d.has_key("name") and d.has_key("value") and d["name"] == "userCmd":
            txtCmd = d["value"]
    
    return txtCmd


def _parseCmd(cmd):
    err = None
    cmd = cmd.strip()
    words = cmd.split()               
            
    if len(words) <= 0:
        return (None, None, "Unknown command")

    cmd = None
    params = None
    numParams = len(words[1:])
    matched = False
    for c in _cmds:
        if c.name == words[0] and c.numParams == numParams:
            cmd = c
            params = words[1:c.numParams+1]
            matched = True
            break;
            
    if not matched:
        err = "Unknown command"
        
    return (cmd, params, err)


def _executeCmd(cmd, params, player):
    """Return: (txt, err, errType)"""
    txt = ""
    
    if cmd.name == "inven":
        txt = "You currently have the following in your inventory:\n"
        inven = player.getInventoryNames()
        for i in inven:
            txt += i + "\n"
        txt = txt[0:len(txt)-1]
        return (txt, None, None)

    if cmd.name == "use":
        if len(params) >= 2:
            return player.getLocation().useWith(params[0], params[1])
        else:
            return player.getLocation().use(params[0])

    if cmd.name == "talk":
        return player.getLocation().talk(params[0])

    if cmd.name == "room":
        txt = "The room contains the following:\n"
        contents = player.getLocation().getRoomContentsLabels()
        for i in contents:
            txt += i + "\n"
        txt = txt[0:len(txt)-1]
        return (txt, None, None)

    if cmd.name == "lookat":
        return player.getLocation().lookat(params[0])

    if cmd.name == "pickup":
        #if len(params) >= 2:
        #    return self._player.getLocation().pickupOn(params[0], params[1])
        #else:
        return player.getLocation().pickUp(params[0])

    err = "cmd.name unknown"
    #logging.error(err)
    raise ValueError(err)
            

def handleCmd(cmdList, player):
    if player.getDead() == True:
        return (None, "You're dead you can't do anything", ErrorType.GAME)
        
    txtCmd = _validateCmd(cmdList)
    if txtCmd == None:
        return (None, 'Broken cmd from client', ErrorType.SYSTEM)

    txtCmd = txtCmd.lower()
    
    (cmd, params, err) = _parseCmd(txtCmd)
    if err != None:
        return (None, err, ErrorType.GAME)
                        
    logging.info("Executing: %s %s" % (cmd.name, params))
    (txt, err, errType) = _executeCmd(cmd, params, player)
    if err != None:
        return (None, err, errType)

    return (txt, None, None)
    
    
