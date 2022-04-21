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
  