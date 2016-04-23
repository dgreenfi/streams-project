function bioinit(){

    document.getElementById("primarypane").innerHTML = "<h1>Bios</h1>";
}

function bio_change(meetup,name,bio){

    document.getElementById("primarypane").innerHTML = "<h1>"+name+"</h1>" +
        "<p>"+bio+"</p>"
    ;
}
