$(document).ready(function() {
  // Calculate the height of the items in the carousel.
  // Fix the height of all items to that height.
  var maxHeight = 45;
  var height = 0;
  $("#news-most-popular-actions .item").each(function(index, item) {
    height = $(item).height();
    // console.log("height of item is " + height);
    if (height > maxHeight){
      maxHeight = height;
    }
  });
  
  $("#news-most-popular-actions").height(maxHeight);
  $(".carousel").carousel();
});