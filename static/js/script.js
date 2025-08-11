  let cart = JSON.parse(localStorage.getItem("cart")) || [];

    function updateCartDisplay() {
      const cartCount = document.getElementById("cart-count");
      let totalQuantity = 0;
      cart.forEach(item => {
        totalQuantity += item.quantity;
      });

      if (totalQuantity > 0) {
        cartCount.textContent = totalQuantity;
        cartCount.style.display = "inline-block";
      } else {
        cartCount.style.display = "none";
      }
    }

    document.addEventListener("DOMContentLoaded", function () {
      const cartButtons = document.querySelectorAll(".cart-btn");

      cartButtons.forEach(button => {
        button.addEventListener("click", () => {
          const productId = button.dataset.productId;
          const productCard = button.closest(".product-card");
          const name = productCard.querySelector("h4").textContent;
          const priceText = productCard.querySelector(".price").textContent;
          const price = parseFloat(priceText.replace("$", ""));

          const existing = cart.find(item => item.id === productId);
          if (existing) {
            existing.quantity += 1;
          } else {
            cart.push({ id: productId, name, price, quantity: 1 });
          }

          localStorage.setItem("cart", JSON.stringify(cart));
          updateCartDisplay();
        });
      });
      
      // Initial display
      updateCartDisplay();
    });
    document.getElementById("cart-icon").addEventListener("click", () => {
      const cartDetails = document.getElementById("cart-details");
      const cartItemsList = document.getElementById("cart-items");

      // Clear previous content
      cartItemsList.innerHTML = "";

      if (cart.length === 0) {
        cartItemsList.innerHTML = "<li>Your cart is empty.</li>";
      } else {
        cart.forEach(item => {
          const li = document.createElement("li");
          li.textContent = `${item.name} - $${item.price} x ${item.quantity}`;
          cartItemsList.appendChild(li);
        });
      }

      // Toggle cart visibility
      cartDetails.style.display = (cartDetails.style.display === "none") ? "block" : "none";
    });