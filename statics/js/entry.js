document.querySelector('.close').addEventListener("click",
    function () {
	    document.querySelector('.bgm').setAttribute("style", "display:none");
});

document.addEventListener("keyup",
    function (event) {
        event.preventDefault();
        if (event.key === "Escape" ) {
            document.querySelector('.close').click();
        }
});