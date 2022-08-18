function createMsgHtml(data){
    var msg = $('<div>').addClass('message');
    
    var avatar = $('<div>').addClass('avatar');
    if(!data['continue_thread'])
    {
        avatar.append($('<img>').attr('src', "/static/img/profile_default.png"));
    }
    else
    {
        avatar.append($('<p>').text(data['time']));
    }
    msg.append(avatar);
    
    var contentBox = $('<div>').addClass('content-box');
    if(!data['continue_thread'])
    {
        var header = $('<div>').addClass('header');
        header.append($('<h3>').text(data['username']));
        header.append($('<p>').text(data['date']));
        contentBox.append(header);
    }
    var content = $('<div>').addClass('content');
    content.text(data['msg']);
    contentBox.append(content);
    msg.append(contentBox);

    $('#messages').append(msg);
}

$(document).ready(()=>{
    var socket = io.connect(window.location.hostname + ":" + port);
    var currRoom = 'General';
    
    socket.on('connect', ()=>{});

    socket.on('message', (data)=>{
        createMsgHtml(data);
        $("#messages, .content-box").scrollTop($("#messages, .content-box")[0].scrollHeight);
    });

    whitespacesRegex = new RegExp("^\\s*$", "g");

    $('#sendBtn').on('click', ()=>{
        // Skip empty messages
        if ($('#msg').val().match(whitespacesRegex) || $('#msg').val() == "") return;
        socket.send({'username': $('#username').val(), 'msg': $('#msg').val()}, currRoom);
        $('#msg').val('');
        $("#messages, .content-box").scrollTop($("#messages, .content-box")[0].scrollHeight);
    });

    $('#joinBtn').on('click', ()=>{
        socket.emit('join', {'username': $('#username').val(), 'room': 'room-1'});
        currRoom = 'room-1';
    });

    $('#msg').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13'){
            $('#sendBtn').click();
        }
    });
});

