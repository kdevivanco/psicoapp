console.log(document.getElementById('my-select'))
var checkboxes = document.querySelectorAll(".dropdown-content input[type=checkbox]");
var inputcheckboxes = document.querySelectorAll(".dropdown-content input")

for (var i = 0; i < checkboxes.length; i++) {
  console.log(checkboxes.value)
  inputcheckboxes[i].addEventListener("change", checkSelection);
}

function checkSelection() {
    var selectedOptions = document.querySelectorAll(".dropdown-content input[type=checkbox]:checked");
    if (selectedOptions.length >= 5) {
      var otherCheckboxes = document.querySelectorAll(".dropdown-content input[type=checkbox]:not(:checked)");
      for (var i = 0; i < otherCheckboxes.length; i++) {
        otherCheckboxes[i].disabled = true;
        this_checkText = document.getElementById("cat-name" + otherCheckboxes[i].value)
        this_checkText.classList.add('distext')
      }
    } else {
      var allCheckboxes = document.querySelectorAll(".dropdown-content input[type=checkbox]");
      for (var i = 0; i < allCheckboxes.length; i++) {
        this_checkText = document.getElementById("cat-name" + allCheckboxes[i].value)
        this_checkText.classList.remove('distext')

        allCheckboxes[i].disabled = false;

      }
    }
  }