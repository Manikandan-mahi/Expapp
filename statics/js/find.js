window.onload = function() {
    document.getElementById("txt_txn").focus();
  };

document.getElementById("txt_txn")
    .addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.key === 'Enter' ) {
        document.getElementById("btn_find").click();
    }
});