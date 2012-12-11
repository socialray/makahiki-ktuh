$(document).ready(function() {
  $("#help-ask-form textarea").keyup(function() {
    if (this.value.length == 0) {
      $("#help-ask-submit").attr("disabled", true);
    }
    else {
      $("#help-ask-submit").attr("disabled", false);
    }
  });

  $('#successModal').modal({
      backdrop: false,
      keyboard: true,
      show: false
  }); 
  // set up event logging
  $('#successModal').on('shown', function() {
      log_js_action("ask_admin", "form", 'feedback-success-open');
  });
  $('#successModal').on('hidden', function() {
      log_js_action("ask_admin", "form", 'feedback-success-close');
  });

  $("#help-ask-submit").click(function() {
    if(! $(this).attr("disabled")) {
      $(this).attr("disabled", true);
      $("#field_url").val(window.location);
      $("#help-ask-spinner").show();
      $.post(this.form.action, $("#help-ask-form").serialize(), function(data) {
//        $("#feedback-success").dialog("open");
    	var modalElement = $('#successModal');
        modalElement.css('margin-top', (modalElement.outerHeight() / 2) * -1);
    	$('#successModal').modal('show');
        $("#help-ask-spinner").hide();
        $("#help-ask-form textarea").val("");
      });

      return false;
    }
  });
});