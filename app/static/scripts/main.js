function loadTextEditor(id){
    CKEDITOR.replace(id);
}

function saveTextEditorValue(id){
    var data = CKEDITOR.instances[id].getData();
    console.log(data);
    document.getElementById('content').value = data;
}