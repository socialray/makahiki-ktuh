$(document).ready(function() {
  var textarea = $("#id_post");
  var post_button = $("#wall-post-submit");
  if (textarea) {
	  textarea.keyup(function() {
		  if (this.value.length === 0 && !post_button.hasClass("disabled")) {
			  post_button.addClass("disabled");
		  }
		  else if (this.value.length > 0 && post_button.hasClass("disabled")){
			  post_button.removeClass("disabled");
		  }
	  });	
  }
  if (post_button) {
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
  }
});