// Get the popup and the button that opens it
var paymentPopup = document.getElementById("paymentPopup");
var makePaymentBtns = document.querySelectorAll(".make-payment");

// Get the close button and payment form elements
var closeBtn = document.querySelector(".close-btn");
var cardPaymentForm = document.getElementById("cardPaymentForm");
var qrPaymentForm = document.getElementById("qrPaymentForm");

// When the user clicks the "Make Payment" button, open the popup
makePaymentBtns.forEach(function(btn) {
  btn.onclick = function() {

 const orderId = btn.dataset.id;
 const orderTotal = btn.dataset.total;

    // Set the order details as properties of the global variable
  window.orderDetails = {
      orderId: orderId,
      orderTotal: orderTotal
    };

// Display the order details
const orderIdElement = document.getElementById("popup_orderId");
const orderTotalElement = document.getElementById("popup_price");
const popup_form1 = document.getElementById("form1");

orderIdElement.textContent = `Order ID: ${orderId}`;
orderTotalElement.textContent = `Total Amount: ${orderTotal}`;
popup_form1.action = "payment/" + orderId + "/"

    paymentPopup.style.display = "block";
  }
});

// When the user clicks the close button, close the popup
closeBtn.onclick = function() {
  paymentPopup.style.display = "none";
}

// When the user clicks outside the popup, close it
window.onclick = function(event) {
  if (event.target == paymentPopup) {
    paymentPopup.style.display = "none";
  }
}

// Show/hide payment forms based on selected payment method
var paymentMethodRadios = document.getElementsByName("paymentMethod");
paymentMethodRadios.forEach(function(radio) {
  radio.addEventListener("change", function() {
    if (this.id === "cardPayment") {
      cardPaymentForm.style.display = "block";
      qrPaymentForm.style.display = "none";
    } else {
      cardPaymentForm.style.display = "none";
      qrPaymentForm.style.display = "flex";
    }
  });
});
