$(document).ready(()=>{
    var socket = io.connect('localhost:5000');
    var currRoom = 'General';
    
    socket.on('connect', ()=>{
        socket.send("User connected!");
    });

    socket.on('message', (data)=>{
        $('#messages').append($('<p>').text(data));
    });

    $('#sendBtn').on('click', ()=>{
        socket.send($('#username').val() + ': ' + $('#msg').val(), currRoom);
        $('#msg').val('');
    });

    socket.on('join_room', (room)=>{
        console.log('@INFO: Joined room');
    });

    $('#joinBtn').on('click', ()=>{
        console.log("@INFO: Trying to join room");
        socket.emit('join', {'username': $('#username').val(), 'room': 'room-1'});
        currRoom = 'room-1';
    });
});

