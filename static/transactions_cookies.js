function setCookie(cookie_name, cookie_value, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires="+d.toUTCString();
    document.cookie = cookie_name + "=" + cookie_value + ";" + expires + ";path=/";
  }
  
  function getCookie(cookie_name) {
    let name = cookie_name + "=";
    let cookie_array = document.cookie.split(';');
    for(let i = 0; i < cookie_array.length; i++) {
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

  function assignTransactionIDToCategory(transaction_id, category_name) {
    categories_dict_string = getCookie("categories");
    var categories_dict;

    if (categories_dict_string != "") {
      categories_dict = JSON.parse(categories_dict_string);
      if (category_name in categories_dict) {
        categories_dict[category_name].push(transaction_id);
      } else {
        categories_dict[category_name] = [transaction_id];
      }
    } else {
      var categories_dict = {
        category_name: transaction_id
      };
    }

    setCookie("categories", JSON.stringify(categories_dict), 365);
  }

  function removeTransactionIDFromCategory(transaction_id, category_name) {
    categories_dict_string = getCookie("categories");
    var categories_dict;

    if (categories_dict_string != "") {
      categories_dict = JSON.parse(categories_dict_string);
    } else {
      if (category_name in categories_dict) {
        transaction_ids_list = categories_dict[category_name];
        categories_dict[category_name] = transaction_ids_list.filter(function(e) { return e !== transaction_id });
      }    
    }
    
    setCookie("categories", JSON.stringify(categories_dict), 365);
  }

  