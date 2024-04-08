// Get the review popup and the button that opens it
var reviewPopup = document.getElementById("reviewPopup");
var leaveReviewBtn = document.querySelectorAll(".leave-review");

var closeBtn = document.querySelector(".close-btn-re");

// When the user clicks the "Leave review" button, open the popup
leaveReviewBtn.forEach(function(btn) {
    btn.onclick = function() {
     const productId = btn.dataset.id;
     const productName = btn.dataset.name;
     const popup_form1 = document.getElementById("review-form");

     //
    const reviewElement = document.getElementById("review-h2");
    reviewElement.textContent = `Leave a Review for ${productName}`;


     popup_form1.action = "review/add/" + productId + "/"

     reviewPopup.style.display = "block";
    }
})

// When the user clicks outside the popup, close it
window.onclick = function(event) {
  if (event.target == reviewPopup) {
    reviewPopup.style.display = "none";
  }
}
// When the user clicks the close button, close the popup
closeBtn.onclick = function() {
  reviewPopup.style.display = "none";
}

   const radioButtons = document.querySelectorAll('input[name="rate"]');
   const hiddenInput = document.getElementById('id_rate');

    // Loop through each radio button
    radioButtons.forEach((radioButton) => {
        // Add event listener for change event
        radioButton.addEventListener('change', () => {
            // Check if the radio button is checked
            if (radioButton.checked) {
                // Get the value of the checked radio button
                 hiddenInput.value = radioButton.value;
            }
        });
    });