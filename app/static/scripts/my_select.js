
console.log(document.getElementById('my_select'))
var checkboxes = document.querySelectorAll(".dropdown-content input[type=checkbox]");

for (var i = 0; i < checkboxes.length; i++) {
  checkboxes[i].addEventListener("change", checkSelection);
}

function checkSelection() {
    var selectedOptions = document.querySelectorAll(".dropdown-content input[type=checkbox]:checked");
    if (selectedOptions.length >= 5) {
      alert("You can only select a maximum of 5 options");
      var otherCheckboxes = document.querySelectorAll(".dropdown-content input[type=checkbox]:not(:checked)");
      for (var i = 0; i < otherCheckboxes.length; i++) {
        otherCheckboxes[i].disabled = true;
      }
    } else {
      var allCheckboxes = document.querySelectorAll(".dropdown-content input[type=checkbox]");
      for (var i = 0; i < allCheckboxes.length; i++) {
        allCheckboxes[i].disabled = false;
      }
    }
  }


