$(document).ready(()=>{
    var socket = io.connect('localhost:8080');
    var currRoom = 'General';
    
    socket.on('connect', ()=>{});

    socket.on('message', (data)=>{
        $('#messages').append($('<p>').text(data));
    });

    $('#sendBtn').on('click', ()=>{
        socket.send($('#username').val() + ': ' + $('#msg').val(), currRoom);
        $('#msg').val('');
    });

    $('#joinBtn').on('click', ()=>{
        socket.emit('join', {'username': $('#username').val(), 'room': 'room-1'});
        currRoom = 'room-1';
    });
});

