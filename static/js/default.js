var editor = CodeMirror.fromTextArea(document.getElementById('codemirror'), {
    lineNumbers: true
});

editor.on('beforeChange', function (cm, obj) {
    var doc = editor.getDoc();
    var cursor = doc.getCursor();

    if (obj.origin === "+delete") {
        if (cursor.ch > 0) {
            $.get("/remove/" + cursor.ch, function () {
                update()
            })
        }
    } else if (obj.origin === "+input") {
        $.get("/insert/" + obj.text[0], {'pos': cursor.ch}, function () {
            update()
        })
    }
});

function update() {
    $.ajax({
        type: "GET",
        url: "/update",
    }).done(function (o) {
        updatetextarea()
    });
}

function updatetextarea() {
    $.ajax({
        type: "GET",
        url: "/get",
    }).done(function (o) {
        var doc = editor.getDoc();
        var cursor = doc.getCursor();
        editor.setValue(o)
        editor.setCursor(cursor)
    });
}
$(document).ready(function () {
    setInterval("updatetextarea()", 1000);
});