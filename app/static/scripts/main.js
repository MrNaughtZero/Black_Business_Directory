// Text Editor for Posts

function loadTextEditor(id){
    CKEDITOR.replace(id);
}

function saveTextEditorValue(id){
    var data = CKEDITOR.instances[id].getData();
    console.log(data);
    document.getElementById('content').value = data;
}

function preloadTextEditor(id, content){
    document.getElementById(id).value = content;
}

// Admin side menu

function menuShowSubPosts(){
    document.getElementsByClassName('hidden-post-links')[0].style.display = 'block';
    document.getElementById('showPostsLink').onclick = menuHideSubPosts;
    
}

function menuHideSubPosts(){
    document.getElementsByClassName('hidden-post-links')[0].style.display = 'none';
    document.getElementById('showPostsLink').onclick = menuShowSubPosts;
}