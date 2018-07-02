$(function(){
  $("#x2").click(()=>{
    $("body").css("width", "50%")
  })
  $("#x1").click(()=>{
    $("body").css("width", "100%")
  })

  $("body").contentEditable = true;
  $(".copy").click((e)=>{
    var target = $(e.target).prev();
    target.css("background-color", "#ffd")
    var range = document.createRange();
    range.selectNode(target[0]);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);
    document.execCommand('copy');
  });
});
