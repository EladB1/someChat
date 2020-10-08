function getTableClone() {
  let table = document.getElementById('userTable');
  let tclone = table.cloneNode(true);
  return tclone;
}

function remove_search_error() {
  let search_res = document.getElementById('search_results');
  if (search_res !== null)
    search_res.remove();
}

async function userSearch(tclone) {
  let username = document.getElementById('user_searchbar').value;
  let table = document.getElementById('userTable');
  remove_search_error();
  if (username === '') {
    table.replaceWith(tclone); // restore full table and exit the function
    return;
  }
  let url = `/contacts/${username}`;
  let req = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    }
  };
  try {
    let response = await fetch(url, req);
    if (!response.ok)
      throw new Error(`Request failed. HTTP Status: ${response.status}`);
    else {
      let response_content = await response.json();
      let json = response_content;
      if (json === null) {
        table.replaceWith(tclone);
        document.body.innerHTML += '<p id="search_results" style="color: #ff0000;">User not found</p>';
        return;
      }
      clearTable();
      let results = `<td id="userid_0" class="userids">${json[0]}</td><td id="username_0" class="usernames">${json[1]}</td>`;
      insertRowIntoTable(results);
    }
  }
  catch (exception) {
    console.error(exception);
  }
}

function clearTable() {
  let table = document.getElementById('userTable');
  let rows = table.getElementsByTagName('tr');
  let len = rows.length;
  for(i = len-1; i > 0; i--) {
    table.deleteRow(i);
  }
}

function insertRowIntoTable(row) {
  let table = document.getElementById('userTable');
  let tableRef = table.getElementsByTagName('tbody')[0];
  let new_row = tableRef.insertRow(tableRef.rows.length);
  new_row.id = 'row_0';
  new_row.class = 'tableRows';
  new_row.innerHTML = row;
}
