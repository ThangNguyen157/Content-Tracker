
var backColor = [];
var color = [];
var ids = [];

function isAdded(id) {
    for(i= 0; i < ids.length; i++) {
        if (id === ids[i]) {
            return true;
        }
    }
    return false;
}

function getIndex(id) {
    for (i = 0; i < ids.length; i++) {
        if (id === ids[i]) {
            return i;
        }
    }
}

function changeColor(id) {
    var tag = document.getElementById(id);
    if (!isAdded(id)) {
        backColor.push(tag.style.backgroundColor);
        tag.style.backgroundColor = "yellow";
        ids.push(id);
    } else {
        var index = getIndex(id);
        tag.style.backgroundColor = backColor[index];
        backColor.splice(index, 1);
        ids.splice(index, 1);
    }
    if (tag.style.color != "black") {
        color.push(tag.style.color);
        tag.style.color = "black";
    } else {
        tag.style.color = color[index];
        color.splice(index, 1);
    }
}

