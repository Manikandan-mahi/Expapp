window.onload = function() {
    document.getElementById("txt_exp").focus();
  };

document.getElementById("txt_exp")
    .addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.key === 'Enter' ) {
        document.getElementById("btn_find").click();
    }
});