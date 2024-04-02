var died=false;

function juice_menu(){
    juice = document.createElement("div");

    dispenser = document.createElement("img");
    dispenser.src = "/sys/images/dispenser.jpg";
    dispenser.classList.add("dispenser")
    dispenser.oncontextmenu="return false";
    dispenser.ondragstart="return false";
    dispenser.onselectstart="return false";
    juice.appendChild(dispenser);

    liq = document.createElement("span");
    liq.classList.add("liq");
    juice.appendChild(liq);

    juice.classList.add("juice")
    juice.oncontextmenu="return false";
    juice.ondragstart="return false";
    juice.onselectstart="return false";
    juice.addEventListener("mousedown",(e)=>{
        const colors= ["red","green","blue"];
        const pbt= [5,497,498]
        const randNum = Math.floor((Math.random()*999)+1);
        var idx = 0;
        for(let i=0;i<colors.length;i++){
            idx += pbt[i];
            if(idx>randNum){
                if(colors[i]=="red"){
                    died=true;
                }
                document.getElementsByClassName("liq")[0].style.background=colors[i];
                break;
            }
        }
    });
    juice.addEventListener("mouseup",(e)=>{
        if(died){
            alert("YOU DIED");
        }
    });

    document.body.appendChild(juice);
}