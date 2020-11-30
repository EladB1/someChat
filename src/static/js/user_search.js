function remove_search_error() {
  let search_res = document.getElementById('search_results');
  if (search_res !== null)
    search_res.remove();
}

// This function has a linear complexity for refreshing the table and for finding the appropriate row to display
// Will try to get this down to logarithmic time using binary search and refresh down to constant time
// Will sort by username
function userSearch() {
  let username = document.getElementById('user_searchbar').value;
  let table = document.getElementById('userTable');
  remove_search_error(); // don't want this showing up twice
  if (username === '') {
    refreshTable(); // restore full table and exit the function
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

function binarySearch_rows(arr, left, right, find) {
  let middle = (left + right) / 2;
  let middle_elem = arr[middle].getElementsByClassName('usernames')[0].innerHTML
  if (left > right)
    return -1; // nothing found; base case
  else if (find.localeCompare(middle_elem) === 1) // greater than
    return binarySearch(arr, middle+1, right, find);
  else if  (find.localeCompare(middle_elem) === -1) // less than
    return binarySearch(arr, left, middle-1, find);
  else if (find.localeCompare(middle_elem) === 0) // equals
    return middle; // found it
}

function userSearch2() { // temporary function to test binary searching the results without breaking anything
  let username = document.getElementById('user_searchbar').value;
  let table = document.getElementById('userTable');
  if (username === '') {
    refreshTable(); // restore full table and exit the function
    remove_search_error();
    return;
  }
  let rows = table.getElementsByTagName('tr');
  let rownum = binarySearch_rows(rows, 1, rows.length-1, username);
  if (rownum === -1) { // not found
    refreshTable(); // This function still runs in linear time, need it to work in constant time for this function to truly be O(logn)
    document.getElementById('search_container').innerHTML += '<p id="search_results" style="color: #ff0000;">User not found</p>';
    return;
  }
  else {
    table.getElementsByClassName('tableRows').style.display = 'none'; // this won't work; row hiding needs to be done faster than linear time for this to be an improvment
    table.getElementById(`row_${rownum}`).style.display = '';
  }
}

// There doesn't seem to be a way to do this any faster than linear time
// Trying to find a way to modify the CSS on the fly to achieve that
function refreshTable() {
  let table = document.getElementById('userTable');
  let rows = table.getElementsByTagName('tr');
  let i;
  for (i = 1; i < rows.length; i++) { // every row except for the header row
    rows[i].style.display = '';
  }
}
