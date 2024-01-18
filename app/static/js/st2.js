function _getangle(e1,e2){
    posx1=e1.offsetLeft-(e1.offsetWidth/2);
	posy1=-(e1.offsetTop-(e1.offsetHeight/2));
    posx2=e2.offsetLeft-(e2.offsetWidth/2);
	posy2=-(e2.offsetTop-(e2.offsetHeight/2));
	if(posx1==posx2){
		if(posy1==posy2){
			return None;
		} else {
			return posy1>posy2 ? -90 : 90;
		}
	}
	if(posy1==posy2){
		return posx1>posx2 ? 180 : 0;
	}
    return Math.atan2(posy2-posy1,posx2-posx1)*180/Math.PI;
}

function setarrowsize() {
    FontSize = parseInt(parseInt(Math.pow(Math.pow(window.innerHeight,2)+Math.pow(window.innerWidth,2),(1/2)))*(100/2094));
    const arrows = document.getElementsByClassName("arrow");
    for(var i=0;i<arrows.length;i++){
        arrows[i].style.fontSize=FontSize.toString()+"px";
        arrows[i].style.marginLeft="-"+(arrows[i].offsetWidth/2).toString()+"px";
        arrows[i].style.marginTop="-"+(arrows[i].offsetHeight/2).toString()+"px";
    }
    for(var i=0;i<arrows.length;i++){
        if(i!=0){
            arrows[i-1].style.transform = "rotate("+(-_getangle(arrows[i-1],arrows[i]))+"deg)";
        }
    }
}
function _onload() {
    document.getElementById("1").style="top: 50%; left: 50%;";
    document.getElementById("2").style="color:black; top: 50%; left: 80%;";
    document.getElementById("3").style="color:black; top: 20%; left: 75%;";
    document.getElementById("4").style="color:black; top: 70%; left: 20%;";
    document.getElementById("5").style="color:black; top: 30%; left: 50%;";
    setarrowsize();
    window.addEventListener("resize",(e)=>{
        setarrowsize();
    });
    document.getElementById("2").addEventListener("click",_arrowclick);
}

function _arrowclick(e){
    if(e.target.id!=document.getElementsByClassName("arrow").length) {
        e.target.style.color="black";
        document.getElementById((parseInt(e.target.id) - 1).toString()).style.color="white";
        document.getElementById((parseInt(e.target.id) + 1).toString()).addEventListener("click", _arrowclick);
    } else {
        document.getElementById((parseInt(e.target.id) - 1).toString()).style.color="white";
        e.target.style.color="yellow";
        window.location.href="/3";
    }
}