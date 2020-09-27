let socket = io.connect(`http://${document.domain}:${location.port}/send`);
socket.on('connect', function(server_msg) {
  let err_ = document.getElementById('error_msg');
  if (err_.innerHTML != '')
    err_.innerHTML = '';
  console.log(server_msg);
  socket.emit('send', {
    data: 'User Connected'
  })
});


socket.on('disconnect', function(server_msg) {
  let err_ = document.getElementById('error_msg');
  err_.innerHTML += server_msg;
  err_.style.color = '#ff0000';
});

function sendMsg() {
  let msg = document.getElementById('msgContents').value;
  if (msg != '') {
    let time = new Date();
    let timestamp = time.getTime();
    socket.emit('message_event', {
      payload: JSON.stringify({'user': username, 'data': msg, 'timestamp': timestamp})
    });
  }
}

socket.on('deliver_message', function(msg) {
  console.log(msg['data']);
  let msgbar = document.getElementById('msgContents');
  let convo = document.getElementById('conversation_history');
  let processed_msg = msg['data'].replace('\n', '<br>');
  convo.innerHTML += `<div class="msg"><p class="user">${username}</p><p class="sent_msgs">${processed_msg}</p></div>`;
  convo.scrollTop = convo.scrollHeight;
  msgbar.value = '';
});

window.onload = function() {
  let msgbar = document.getElementById('msgContents');
  msgbar.addEventListener('keyup', function(event) {
    if (event.keyCode === 13 && !event.shiftKey) // enter key
      document.getElementById('send').click();
  });
};
