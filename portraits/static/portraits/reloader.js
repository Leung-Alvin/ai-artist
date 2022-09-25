setInterval(function() {
    filename = file_url;
    name = filename.substring(0, filename.lastIndexOf('.'));
    ext = filename.substring(filename.lastIndexOf('.'));
    var d1 = new Date();
    var myImageElement = document.getElementById('AIRendition');
    myImageElement.src = name +'final' + ext  + '?rand=' + d1.getTime();
}, 1000);
