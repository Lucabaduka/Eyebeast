// Eyebeast search functions

const init = function(){
    document.getElementById('button-search').addEventListener('click', send);
}

const send = function(ev) {

    var region_name = document.getElementById("search");
    region_name.value = region_name.value.split("https://www.nationstates.net/region=").join("")
    region_name.value = region_name.value.split(" ").join("_").toLowerCase();
    return region_name.value;

}

function copityopity() {

    // get the thingies
    var copyText = document.querySelectorAll(".wfe:not(.inactive)");
    navigator.clipboard.writeText(copyText[0].innerText);
  
    // change the thingies
    document.getElementById('copy').innerHTML = "Copied";
    document.getElementById('copy').classList.add('copied');
  
}

document.addEventListener('DOMContentLoaded', init);
