function warn_set() {
    var warn_op = 0;
    var wart = "";
    const warn_txt = document.getElementById("display_warning");
    var warnmsg="절대건드리지마시오".split('')

    function display_off() {
        if (warn_op > 0) {
            warn_op -= 0.025;
            warn_txt.style.opacity = warn_op;
        } else if (warn_op < 0) {
            warnmsg="절대건드리지마시오".split('')
            warn_txt.innerHTML = "";
            wart = "";
        }
    }

    function display_warning() {
        warn_op = 1;
        wart += this.id;
        warnmsg[this.id-1]='';
        warn_txt.innerHTML = warnmsg.join('');
        wart_tmp = wart.split('').sort().join('')
        console.log(wart, wart_tmp)
        if (wart_tmp == "1267") {
            document.location.href = "/2";
        }
    }

    var keypads = document.getElementsByClassName("keypad");
    for (var i = 0; i < keypads.length; i++) {
        keypads[i].addEventListener("click", display_warning);
    }
    const warn_timer = setInterval(display_off, 20);
}