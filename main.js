$(function(){
    $(".body").click((e)=>{
    e.target.contentEditable = true;
    var range = document.createRange();
    range.selectNode(e.target);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);
    document.execCommand('copy');
});
});
