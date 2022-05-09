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
 * Saves a transaction entry(a row in the transactions table) to local storage and associates it with a category. The 
 * local storage object(key: categories_entire_string) represents a dictionary of dictionaries, where the outer dictionary's key
 * is the category_name, and the inner dictionary maps transaction_ids(keys) to entire transaction entries(where the transaction
 * entries is an asterisk(*) deliminated string consisting of the transaction_id, member_name, member_district, etc).
 * @param {*} category_name - the name of the category that this transaction entry was assigned to, used a key in categories_dict
 * @param {*} transaction_id - the id of the transaction entry
 * @param {*} member_name - the member name of the transaction entry
 * @param {*} member_district - the member district of the transaction entry
 * @param {*} company - the company of the transaction entry
 * @param {*} ticker - the ticker of the transaction entry
 * @param {*} transaction_type - S or P
 * @param {*} transaction_date - the date of the transaction entry
 * @param {*} value_lb - the lower bound of the transaction entry
 * @param {*} value_ub - the upper bound of the transaction entry
 * @param {*} description - the description of the transaction try
 * @param {*} link - the link of the transaction entry
 * @returns 
 */
function assignTransactionEntryToCategory(category_name, transaction_id, member_name, member_district, company, ticker, transaction_type,
  transaction_date, value_lb, value_ub, description, link) {
  if (category_name === "") {
    return;
  }
  categories_dict_string = localStorage.getItem("categories_entire_entry");
  var categories_dict = {};
  transaction_entry_string = "" + transaction_id + "*" + member_name + "*" + member_district + "*" +
    company + "*" + ticker + "*" + transaction_type + "*" + transaction_date + "*" + value_lb + "*" + value_ub + "*" + description + "*" + link + "*" + category_name;
  if (categories_dict_string != null) {
    categories_dict = JSON.parse(categories_dict_string);
    if (category_name in categories_dict) {
      if (!categories_dict[category_name].hasOwnProperty(transaction_id)) {
        categories_dict[category_name][transaction_id] = transaction_entry_string;
      }
    } else {
      categories_dict[category_name] = {};
      categories_dict[category_name][transaction_id] = transaction_entry_string;
    }
  } else {
    categories_dict[category_name] = {};
    categories_dict[category_name][transaction_id] = transaction_entry_string;
  }
  localStorage.setItem("categories_entire_entry", JSON.stringify(categories_dict));
}
/**
 * Deletes the key value pair(category_name, transaction_entry) from the categories_entire_entry local storage object
 * @param {*} category_name - name of the category that this entry should be deleted from
 * @param {*} transaction_id - transaction_id of the entry
 * @returns 
 */

function removeTransactionEntryFromCategory(category_name, transaction_id) {
  if (category_name === "") {
    return;
  }
  categories_dict_string = localStorage.getItem("categories_entire_entry");
  var categories_dict = {};
  if (categories_dict_string != null) {
    categories_dict = JSON.parse(categories_dict_string);
    if (category_name in categories_dict) {
      if (categories_dict[category_name].hasOwnProperty(transaction_id)) {
        delete categories_dict[category_name][transaction_id];
      }
    }
  }
  localStorage.setItem("categories_entire_entry", JSON.stringify(categories_dict));
}

/**
 * Adds the transaction to its category if the toggle_value is not checked, else it deletes the
 * transaction from its category.
 * @param transaction_id - the unique id of the transaction that would be associated with category_name
 * @param category_name - the name of the category
 * @param toggle_element - the ID of the toggleable button element
 */
function callCorrectCookieFunction(transaction_id, category_name, toggle_element, member_name, member_district, company, ticker, transaction_type,
  transaction_date, value_lb, value_ub, description, link) {
  if (category_name === "") {
    return;
  }
  // If the class 'active' is included in the element, the user clicked the toggle and wants to add to a category
  if (document.getElementById(toggle_element).className.split(' ').includes('active')) {
    assignTransactionIDToCategory(transaction_id, category_name, member_name, member_district, company, ticker, transaction_type,
      transaction_date, value_lb, value_ub, description, link);
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
function assignTransactionIDToCategory(transaction_id, category_name, member_name, member_district, company, ticker, transaction_type,
  transaction_date, value_lb, value_ub, description, link) {
  if (category_name === "") {
    return;
  }
  assignTransactionEntryToCategory(category_name, transaction_id, member_name, member_district, company, ticker, transaction_type,
    transaction_date, value_lb, value_ub, description, link);

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
  if (category_name === "") {
    return;
  }
  removeTransactionEntryFromCategory(category_name, transaction_id);
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
    + encodeURI(document.representative_search_form.tradeCount.value) + ","
    + encodeURI(document.representative_search_form.purchaseCount.value) + ","
    + encodeURI(document.representative_search_form.saleCount.value) + ","
    + encodeURI(document.representative_search_form.avgPurchaseTransVal.value) + ","
    + encodeURI(document.representative_search_form.avgSaleTransVal.value) + ","
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

/**
 * Saves advanced searches that were executed to cookies
 * @param {*} cookie_name - name of the cookie(it can be for transactions, representative, or company)
 */

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

/**
 * Generates the table to be showed to the user when a category button is clicked
 * @param {*} category_name - name of the category button that was clicked
 * @returns 
 */
function createCategoryTable(category_name) {
  if (category_name === "") {
    return;
  }
  categories_entire_entry_string = localStorage.getItem("categories_entire_entry");
  if (categories_entire_entry_string != null) {
    categories_dict_dict = JSON.parse(categories_entire_entry_string);
    if (category_name in categories_dict_dict) {
      entries_array = [];
      category_dict = categories_dict_dict[category_name];

      Object.keys(category_dict).forEach(function (key) {
        entries_array.push(category_dict[key].split("*"));
      });


      data = document.getElementById('data');
      head = document.getElementsByTagName('thead')[0];
      console.log(head);
      s = "<tbody>";

      for (let i = 0; i < entries_array.length; i++) {
        s += "<tr class='odd'>";
        for (let j = 1; j < entries_array[i].length; j++) {
          if (j == 5) { // Type column
            if (entries_array[i][j] == "S") {
              s += `<td>Sale</td>`;
            } else {
              s += `<td>Purchase</td>`;
            }
          }
          else if (j == 7 || j == 8) { // Value Lower Bound and Value Upper Bound col
            formatter = new Intl.NumberFormat('en-US', {
              style: "currency",
              currency: "USD"
            });
            s += `<td>${formatter.format(entries_array[i][j])}</td>`;

          }
          else if (j == 9) { // Description col
            if (entries_array[i][j] != "None") {
              s += `<td><a href=${entries_array[i][j]}>Description</a></td>`;
            } else {
              s += `<td>${entries_array[i][j]}</td>`;
            }
          } else if (j == 10) { // Link col 
            s += `<td><a href=${entries_array[i][j]}>Source</a></td>`;
          } else {
            s += `<td>${entries_array[i][j]}</td>`;
          }
        }
        s += "</tr>";
      }
      s += "</tbody>";
      data.innerHTML = s;
    }
  }
  var table = $('#data').DataTable();
  table.destroy();
  
  table = $('#data').DataTable( {
    buttons: [
      { extend: 'csv', className: 'btn btn-primary', exportOptions: { columns: [0, 1, 2, 3, 4, 5, 6, 7] } },
      { extend: 'pdf', className: 'btn btn-primary', exportOptions: { columns: [0, 1, 2, 3, 4, 5, 6, 7] } }
    ],
    retrieve: true
  });
  table.buttons().container().appendTo('#data_wrapper .col-md-6:eq(0)');
}

