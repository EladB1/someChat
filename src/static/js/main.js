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
