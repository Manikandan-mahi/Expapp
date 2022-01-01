document.querySelector('.close_exp').addEventListener("click",
    function () {
	    document.querySelector('.bgm_exp').setAttribute("style", "display:none");
});

document.addEventListener("keyup",
    function (event) {
        event.preventDefault();
        if (event.key === "Escape" ) {
            document.querySelector('.close_exp').click();
        }
});

document.querySelector('.close_inc').addEventListener("click",
    function () {
	    document.querySelector('.bgm_inc').setAttribute("style", "display:none");
});

document.addEventListener("keyup",
    function (event) {
        event.preventDefault();
        if (event.key === "Escape" ) {
            document.querySelector('.close_inc').click();
        }
});
