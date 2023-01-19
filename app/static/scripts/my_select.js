

$(document).ready(function() {
  $("#category").on("change", function() {
    if($("#category option:selected").length >= 5) {
      $("#category option:not(:selected)").attr("disabled", "disabled");
    } else {
      $("#category option").removeAttr("disabled");
    }
  });
});