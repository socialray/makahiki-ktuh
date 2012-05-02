$(document).ready(function() {
  var textarea = $("#id_post");
  var post_button = $("#wall-post-submit");
  textarea.keyup(function() {
    if (this.value.length === 0 && !post_button.hasClass("disabled")) {
      post_button.addClass("disabled");
    }
    else if (this.value.length > 0 && post_button.hasClass("disabled")){
      post_button.removeClass("disabled");
    }
  });
  
  post_button.addClass("disabled");
  
  post_button.click(function() {
    if (!post_button.hasClass("disabled")) {
      $.post(this.form.action, $("#news-post-form").serialize(), function(data) {
        if (data.message) {
          $("#wall-post-errors").html(data.message);
        }
        else {
          $("#wall-post-errors").html("");
          if ($("#wall-no-posts").is(":visible")) {
            $("#wall-no-posts").hide();
          }
          $(data.contents).hide().prependTo("#wall-posts").fadeIn();
          textarea.val("");
          post_button.addClass("disabled");
        }
      });
    }
    return false;
  });
  
  // Calculate the height of the items in the carousel.
  // Fix the height of all items to that height.
  var maxHeight = 45;
  var height = 0;
  $("#news-most-popular-actions .item").each(function(index, item) {
    height = $(item).height();
    console.log("height of item is " + height);
    if (height > maxHeight){
      maxHeight = height;
    }
  });
  
  $("#news-most-popular-actions").height(maxHeight);
  $(".carousel").carousel();
});