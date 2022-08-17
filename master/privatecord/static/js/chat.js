function createMsgHtml(data){
    var msg = $('<div>').addClass('message');
    
    var avatar = $('<div>').addClass('avatar');
    avatar.append($('<img>').attr('src', "/static/img/profile_default.png"));
    msg.append(avatar);
    
    var contentBox = $('<div>').addClass('content-box');
    var header = $('<div>').addClass('header');
    header.append($('<h3>').text(data['username']));
    header.append($('<p>').text(data['date']));
    contentBox.append(header);
    var content = $('<div>').addClass('content');
    content.text(data['msg']);
    contentBox.append(content);
    msg.append(contentBox);

    $('#messages').append(msg);
}

$(document).ready(()=>{
    var socket = io.connect('localhost:8080');
    var currRoom = 'General';
    
    socket.on('connect', ()=>{});

    socket.on('message', (data)=>{
        createMsgHtml(data);
        $("#messages, .content-box").scrollTop($("#messages, .content-box")[0].scrollHeight);
    });

    $('#sendBtn').on('click', ()=>{
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
            console.log('Test');
            $('#sendBtn').click();
        }
    });
});

