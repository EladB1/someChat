function sendMsg() {
	let msg = document.getElementById('msgContents').value;
  let convo = document.getElementById('conversation_history');
  // Even though the code below is only for testing, it's still an XSS vulnerability
  /*if (msg != '')
  	convo.innerHTML += `<p class="msg">${msg}</p>`;
  */
}
