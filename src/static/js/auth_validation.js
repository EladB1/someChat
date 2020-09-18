function passwords_match() {
	let psswd = document.getElementById('password_input');
  let confirm = document.getElementById('confirm_password_input');
  return confirm.value === psswd.value;
}

function handle_registration_submit() {
	let err = document.getElementById('errorMessages');
  err.innerHTML = '';
  check = passwords_match();
  if (!check)
  	err.innerHTML += 'Passwords do not match.<br>';
  return check;
}
