function remove_search_error() {
  let search_res = document.getElementById('search_results');
  if (search_res !== null)
    search_res.remove();
}

function userSearch() {
  let username = document.getElementById('user_searchbar').value;
  let table = document.getElementById('userTable');
  if (username === '') {
    refreshTable(); // restore full table and exit the function
    remove_search_error();
    return;
  }
  let rows = table.getElementsByTagName('tr');
  let rowFound = false;
  let i;
  for (i = 1; i < rows.length; i++) { // don't want to change the headers
    if (rows[i].getElementsByClassName('usernames')[0].innerHTML !== username)
      rows[i].style.display = 'none';
    else {
      rowFound = true;
      rows[i].style.display = '';
    }
  }
  if (!rowFound) {
    refreshTable();
    document.getElementById('search_container').innerHTML += '<p id="search_results" style="color: #ff0000;">User not found</p>';
  }
}

function refreshTable() {
  let table = document.getElementById('userTable');
  let rows = table.getElementsByTagName('tr');
  let i;
  for (i = 1; i < rows.length; i++) { // every row except for the header row
    rows[i].style.display = '';
  }
}
