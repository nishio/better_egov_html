$(function(){
  $("body").contentEditable = true;
  $(".copy-button").click((e)=>{
    var target = document.getElementById($(e.target).attr("target"));
    $(target).css("background-color", "#ffd")
    var range = document.createRange();
    range.selectNode(target);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);
    document.execCommand('copy');
  });

  $("#x2").click(()=>{
    $("body").css("width", "50%")
  })
  $("#x1").click(()=>{
    $("body").css("width", "100%")
  })
});
