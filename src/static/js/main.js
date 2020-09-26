async function ajax_post_req(body, url) {
  reqBody = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: body
  };
  try {
    let response = await fetch(url, reqBody);
    if (!response.ok)
      throw new Error(`Request failed. HTTP Status: ${response.status}`);
    else {
      let resp_content = await response.json();
      return resp_content;
    }
  }
  catch (exception) {
    console.error(exception);
  }
}

async function sendMsg() {
	let msg = document.getElementById('msgContents').value;
  let convo = document.getElementById('conversation_history');
  let json = JSON.stringify({'message': msg});
  if (msg != '') {
      let text = await ajax_post_req(json, '/send');
      convo.innerHTML += `<p class="msg">${text}</p>`
  }
}

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

function sendMsg2() {
  let msg = document.getElementById('msgContents').value;
  if (msg != '') {
    socket.emit('message_event', {
      payload: JSON.stringify({'data': msg})
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
