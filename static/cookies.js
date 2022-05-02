/*JS functions to set and remove cookies. Used to help implement the functionality of saving transactions into custom categories.*/

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
 * Updates the innerHTML of the button to indicate whether to add a transaction to a category
 * or delete a transaction to a category
 * @param toggle_value - whether or not the toggle is checked
 * @param button_element - the categories butten element
 */
function updateCategoryButton(toggle_value, button_element) {
  if (!toggle_value) {
    button_element.innerHTML = "Save";
  } else {
    button_element.innerHTML = "Delete";
  }
}

/**
 * Adds the transaction to its category if the toggle_value is not checked, else it deletes the
 * transaction from its category.
 * @param transaction_id - the unique id of the transaction that would be associated with category_name
 * @param category_name - the name of the category
 * @param toggle_element - the ID of the toggleable button element
 */
function callCorrectCookieFunction(transaction_id, category_name, toggle_element) {
  if (category_name === "") {
    return;
  }
  // If the class 'active' is included in the element, the user clicked the toggle and wants to add to a category
  if (document.getElementById(toggle_element).className.split(' ').includes('active')) {
    assignTransactionIDToCategory(transaction_id, category_name);
  } else {
    removeTransactionIDFromCategory(transaction_id, category_name);
  }
}

/** 
 * Adds the transaction_id to a dictionary where the key is category_name and value is a list of all transaction_ids
 * in that category
 * @param transaction_id - the unique id of the transaction that would be associated with category_name
 * @param category_name - the name of the category
 **/
function assignTransactionIDToCategory(transaction_id, category_name) {
  if (category_name === "") {
    return;
  }

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
  alert("Added transaction " + transaction_id + " to category " + category_name);
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

      alert("Deleted transaction " + transaction_id + " from category " + category_name);
      setCookie("categories", JSON.stringify(categories_dict), 365);
    }
  }
}


function getAdvancedSearchTransaction() {
  return encodeURI(document.transaction_search_form.member_name.value) + ","
    + encodeURI(document.transaction_search_form.distrNum.value) + ","
    + encodeURI(document.transaction_search_form.company.value) + ","
    + encodeURI(document.transaction_search_form.ticker.value) + ","
    + encodeURI(document.transaction_search_form.lowerBound.value) + ","
    + encodeURI(document.transaction_search_form.upperBound.value) + ","
    + encodeURI(document.transaction_search_form.transType.value);
}

function getAdvancedSearchRepresentative() {
  return encodeURI(document.representative_search_form.member_name.value) + ","
    + encodeURI(document.representative_search_form.ticker.value) + ","
    + encodeURI(document.representative_search_form.tradeCount.value) + ","
    + encodeURI(document.representative_search_form.purchaseCount.value) + ","
    + encodeURI(document.representative_search_form.saleCount.value) + ","
    + encodeURI(document.representative_search_form.avgTransactionVal.value) + ","
    + encodeURI(document.representative_search_form.purchaseLowerBound.value) + ","
    + encodeURI(document.representative_search_form.purchaseUpperBound.value) + ","
    + encodeURI(document.representative_search_form.saleLowerBound.value) + ","
    + encodeURI(document.representative_search_form.saleUpperBound.value);
}

function getAdvancedSearchCompany() {
  return encodeURI(document.company_search_form.company.value) + ","
    + encodeURI(document.company_search_form.ticker.value) + ","
    + encodeURI(document.company_search_form.transCount.value) + ","
    + encodeURI(document.company_search_form.memberCount.value) + ","
    + encodeURI(document.company_search_form.purchaselb.value) + ","
    + encodeURI(document.company_search_form.purchaseub.value) + ","
    + encodeURI(document.company_search_form.salelb.value) + ","
    + encodeURI(document.company_search_form.saleub.value);
}

function setAdvancedSearchCookie(cookie_name) {
  var search_cookie_str = getCookie(cookie_name);
  var search_cookie_list = [];
  if (search_cookie_str !== "") {
    search_cookie_list = JSON.parse(search_cookie_str);
  }
  switch (cookie_name) {
    case "advanced_search_transaction":
      search_cookie_list.push(getAdvancedSearchTransaction());
      setCookie("advanced_search_transaction", JSON.stringify(search_cookie_list), 365);
      break;
    case "advanced_search_representative":
      search_cookie_list.push(getAdvancedSearchRepresentative());
      setCookie("advanced_search_representative", JSON.stringify(search_cookie_list), 365);
      break;
    case "advanced_search_company":
      search_cookie_list.push(getAdvancedSearchCompany());
      setCookie("advanced_search_company", JSON.stringify(search_cookie_list), 365);
      break;
  }
}

function setAdvancedSearchTransactionCookie() {
  setAdvancedSearchCookie("advanced_search_transaction");
}

function setAdvancedSearchRepresentativeCookie() {
  setAdvancedSearchCookie("advanced_search_representative");
}

function setAdvancedSearchCompanyCookie() {
  setAdvancedSearchCookie("advanced_search_company");
}
