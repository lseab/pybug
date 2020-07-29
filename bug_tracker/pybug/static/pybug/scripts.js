function getPaging(str) {
    $("#loading-content").load("dataSearch.php?"+str, hideLoader);
  }

/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function actionMenu() {
    document.getElementById("actionMenu").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

// JQuery function to make rows clickable
$(document).ready(function($) {
  $(".clickable-row").click(function() {
      window.location = $(this).data("href");
  });
});

// Submit form when out of focus 
$('form :input').blur(function() {
  console.log($(this).closest('form'))
  $(this).closest('form').submit();
});