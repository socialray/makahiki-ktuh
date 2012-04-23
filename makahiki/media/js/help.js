$(document).ready(function() {
  $("#help-ask-form textarea").keyup(function() {
    if (this.value.length == 0) {
      $("#help-ask-submit").attr("disabled", true);
    }
    else {
      $("#help-ask-submit").attr("disabled", false);
    }
  });

  $("#help-ask-submit").click(function() {
    if(! $(this).attr("disabled")) {
      $(this).attr("disabled", true);
      $("#field_url").val(window.location);
      $("#help-ask-spinner").show();
      $.post(this.form.action, $("#help-ask-form").serialize(), function(data) {
        $("#feedback-success").dialog("open");
        $("#help-ask-spinner").hide();
        $("#help-ask-form textarea").val("");
      });

      return false;
    }
  });
});