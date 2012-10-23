function setErr(err) {
    jQuery('#userCmd').addClass("error")
    jQuery('#chat').html(err);
}

function clearErr() {
    jQuery('#userCmd').removeClass("error");
    jQuery('#chat').html(" ");
}

function recvDataErr() {
    alert("Error contacting server, this might be due to a bug or other maintenance");
}

function recvData(data) {        
    if( (!data.hasOwnProperty("name")) ||
        (!data.hasOwnProperty("txt")) ||
        (!data.hasOwnProperty("errType")) || 
        (!data.hasOwnProperty("err")) ) {
        
       recvDataErr();
    }
    
    if(data.errType == "SYSTEM") {
        recvDataErr();
        return;
    }
        
    if(data.errType == "GAME") {
        setErr(data.err);
        return;
    }

    jQuery('#roomName').html(data.name);   
    jQuery('#roomDescript').html(data.txt);
    jQuery('#userCmd').val("");                
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {        
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {                
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


//TODO: rate limit ajax requests?
jQuery(document).ready(function() {
    jQuery('#userCmd').click(clearErr);
    
    jQuery('#sendCmd').click(function() {
        clearErr();
        userData = JSON.stringify(jQuery('#userControls').serializeArray());
        //userData = "blah"
        jQuery.ajax({  
            beforeSend: function(xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    // Only send the token to relative URLs i.e. locally.
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
                return true
            },        
            url: "/game/",
            type: "POST",            
            processData: false,
            contentType: "application/json",
            data: userData,
            error: recvDataErr,
            success: recvData,
            
        });
        return false;

    });
});
