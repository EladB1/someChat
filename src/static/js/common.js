// Javascript to be used throughout the full web app

// Timeout the displaying of feedback from the server
function hide_server_message() {
  let banner = document.getElementById('backend_messages');
  if (banner == null)
    return;
  let time = 10000; // time in ms
  setTimeout(function() {
    banner.remove();
  }, time);
}

// Run code when the page finishes loading
document.addEventListener('DOMContentLoaded', function() { hide_server_message() });
