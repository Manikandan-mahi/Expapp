function show() {
    document.getElementById('container').setAttribute("style", "display:flex");
}

function addexpense() {
    var expense_name = prompt("Please enter the expense name ");
    var amount = prompt("Please enter the amount ")
    var ddate = document.getElementById('appdate').value;
    var sdate = ddate.toString();
    if (amount === null || typeof amount ==="") { amount = 0 }
    else { amount = Number(amount) }
    window.location.href ="/add/" + expense_name + "/" + amount + "/" + sdate;
}

function addexp()
{
    var expense_name = document.getElementById('txt_expname').value;
    var amount = document.getElementById('txt_expamt').value;
    var desc = document.getElementById('txt_description').value;
    var ddate = document.getElementById('appdate').value;
    var sdate = ddate.toString();
    if (amount === null || typeof amount ==="") { amount = 0 }
    else { amount = Number(amount) }

    if (desc === null || desc === "") { desc = "None" }
    window.location.href ="/add/" + expense_name + "/" + amount +"/"+ desc + "/" + sdate;
}

function deleteexpense(expid) {
    var ddate = document.getElementById('appdate').value;
    var sdate = ddate.toString();
    window.location.href = "/delete/"+expid+"/"+sdate;
}

function viewall()
{
    var ddate = document.getElementById('appdate').value;
    var sdate = ddate.toString();
    window.location.href = "/home/" + sdate;
   // document.getElementById('appdate').value=ddate;
}

function logout()
{
    window.location.href = "/logout/";
}