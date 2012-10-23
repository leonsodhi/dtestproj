#Django imports
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils import simplejson
from django.core.exceptions import ObjectDoesNotExist

import logging
logger = logging.getLogger(__name__)

#App imports
import engine.game
from engine.err import ErrorType

#TODO: need transactions - what if it crashes after part of the data has been inserted


def _createResponse(name, descript, errTxt, errType):
    err = ""
    errTypeTxt = ""
    if errType == ErrorType.GAME:
        err = errTxt
        errTypeTxt = "GAME"                
    elif errType == ErrorType.SYSTEM:
        errTypeTxt = "SYSTEM"
    elif errType == None:
        pass
    else:
        err = "Unknown errType %s" % errType
        logging.error(err)
        raise ValueError(err)

    response = {"name": name, "txt": descript, "err": err, "errType" : errTypeTxt}
    return simplejson.dumps(response)


def _showRoomPost(request, player):
    jsonData = None
    try:
        jsonData = simplejson.loads(request.raw_post_data)
    except:
        logging.error("json.loads(data) failed")
        resp = _createResponse("", "", "", ErrorType.SYSTEM)
        return HttpResponse(resp, mimetype='application/json')
                
    (descript, err, errType) = engine.game.handleCmd(jsonData, player)
    if err != None:
        if errType == ErrorType.SYSTEM:
            logging.error("engine.game.handleCmd(jsonData) failed")
        resp = _createResponse("", "", err, errType)
        return HttpResponse(resp, mimetype='application/json')    

    roomName = player.getLocation().getName()    
    resp = _createResponse(roomName, descript, "", None)
    return HttpResponse(resp, mimetype='application/json')            


def _showRoomGet(request, player):    
    currLocation = player.getLocation()
    cmdHelp = engine.game.getCmdHelp()
    room = { 
        'name': currLocation.getName(), 
        'description' : currLocation.getDescription(),
    }
    return direct_to_template(request, 'show_room.html', {
        'room': room,
        'cmdHelp': cmdHelp,
    })


@login_required
def showRoom(request):
    player = None
    try:
        player = request.user.get_profile()
    except ObjectDoesNotExist:
        player = engine.game.createPlayer(request.user)
        
    if request.method == 'POST':
        return _showRoomPost(request, player)
    else:   
        return _showRoomGet(request, player)


@login_required
def restart(request):    
    try:
        player = request.user.get_profile()
        player.delete()
    except ObjectDoesNotExist:
        pass
    #engine.game.createPlayer(request.user)
    return HttpResponseRedirect("/game/")

def registerUser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            newUser = form.save()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            login(request, new_user)
            return HttpResponseRedirect("/game/")
    else:
        form = UserCreationForm()
    return direct_to_template(request, 'registration/register.html', {'form': form,})

