/** 
 * Sets a cookie
 * @param cookie_name - the name of the cookie 
 * @param cookie_value - the value of the cookie 
 * @param exdays - the number of days before the cookie is set to expire
 **/
function setCookie(cookie_name, cookie_value, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  let expires = "expires=" + d.toUTCString();
  document.cookie = cookie_name + "=" + cookie_value + ";" + expires + ";path=/";
}


/** 
 * Retrives a cookie value
 * @param cookie_name - the name of the cookie 
 * @returns {string} - the value of the cookie
 **/
function getCookie(cookie_name) {
  let name = cookie_name + "=";
  let cookie_array = document.cookie.split(';');
  for (let i = 0; i < cookie_array.length; i++) {
    let cookie_value = cookie_array[i];
    while (cookie_value.charAt(0) == ' ') {
      cookie_value = cookie_value.substring(1);
    }
    if (cookie_value.indexOf(name) == 0) {
      return cookie_value.substring(name.length, cookie_value.length);
    }
  }
  return "";
}

/** 
 * Adds the transaction_id to a dictionary where the key is category_name and value is a list of all transaction_ids
 * in that category
 * @param transaction_id - the unique id of the transaction that would be associated with category_name
 * @param category_name - the name of the category
 **/
function assignTransactionIDToCategory(transaction_id, category_name) {
  categories_dict_string = getCookie("categories");
  var categories_dict = {};

  if (categories_dict_string != "") {
    categories_dict = JSON.parse(categories_dict_string);
    if (category_name in categories_dict) {
      categories_dict[category_name].push(transaction_id);
    } else {
      categories_dict[category_name] = [transaction_id];
    }
  } else {
    categories_dict[category_name] = [transaction_id];
  }

  setCookie("categories", JSON.stringify(categories_dict), 365);
}

/** 
 * Removes the transaction_id from a dictionary where the key is category_name and value is a list of all transaction_ids
 * in that category
 * @param transaction_id - the unique id of the transaction that would be associated with category_name
 * @param category_name - the name of the category
 **/
function removeTransactionIDFromCategory(transaction_id, category_name) {
  categories_dict_string = getCookie("categories");
  var categories_dict;

  if (categories_dict_string != "") {
    categories_dict = JSON.parse(categories_dict_string);
    if (category_name in categories_dict) {
      transaction_ids_list = categories_dict[category_name];
      categories_dict[category_name] = transaction_ids_list.filter(function (e) { return e !== transaction_id });
      
      setCookie("categories", JSON.stringify(categories_dict), 365);
    }
  }
}


