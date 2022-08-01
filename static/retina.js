// Eyebeast toggle functions

const snapMax = Number(document.getElementById('length').innerHTML);
var snapIndex = document.getElementById('indexBox').value;

function uppity(){
    snapIndex++;
    document.getElementById('indexBox').value = snapIndex;

    // Make sure the button functionality makes sense
    var current = document.getElementById('indexBox').value;
    if (Number(current) > 1) {
        document.getElementById("forward").disabled = false;
    }
    if (Number(current) == snapMax) {
        document.getElementById("backward").disabled = true;
    }

    // Toggle what is visible to the user
    let items = ["regions", "stamps", "flags", "wfes", "tags", "banners", "ros"];
    for (obj in items){
        var fetchthing = document.getElementById(items[obj]);
        fetchthing.querySelector(`.${items[obj]}:nth-child(${snapIndex-1})`).classList.add('inactive');
        fetchthing.querySelector(`.${items[obj]}:nth-child(${snapIndex})`).classList.remove('inactive');
    }
}

function downity(){
    snapIndex--;
    document.getElementById('indexBox').value = snapIndex;

    // Make sure the button functionality makes sense
    var current = document.getElementById('indexBox').value;
    if (Number(current) < snapMax) {
        document.getElementById("backward").disabled = false;
    }
    if (Number(current) == 1) {
        document.getElementById("forward").disabled = true;
    }

    // Toggle what is visible to the user
    let items = ["regions", "stamps", "flags", "wfes", "tags", "banners", "ros"];
    for (obj in items){
        var fetchthing = document.getElementById(items[obj]);
        fetchthing.querySelector(`.${items[obj]}:nth-child(${snapIndex+1})`).classList.add('inactive');
        fetchthing.querySelector(`.${items[obj]}:nth-child(${snapIndex})`).classList.remove('inactive');
    }
}