// Check if user already has items added to the basket. If so, display them, else, create a new array.
var cartItems = localStorage.getItem("cartItems");
var totalPrice = 0.0;
// innerId is used to index items in the basket, in order to possibly allow for deleting specific elements by the user.
var innerId = localStorage.getItem("innerId");

if (!innerId)
{
  // If there is no innerId in localStorage, it means that the user doesn't have any products in basket yet.
  innerId = 0;
}

if (cartItems)
{
  // JSON is stored in the localStorage as a string.
  cartItems = JSON.parse(cartItems);
  cartItems.forEach(item => {
    addToShoppingCart(item);
  });
}
else
{
  cartItems = [];
}

document.addEventListener("DOMContentLoaded", () => {

  document.addEventListener("click", function(event) {

    // This will be called when user clicks on one of the items in order to add it to the basket.
    if (event.target.matches(".addToBasket"))
    {
      // Create JSON containing information about the chosen product and add it to the cartItems.
      let itemObj = {
        "itemType": event.target.dataset.type,
        "itemSize": event.target.dataset.size,
        "itemName": event.target.dataset.name,
        "itemPrice": event.target.dataset.price,
        "itemId": event.target.dataset.id,
        "innerId": innerId
      };

      innerId++;
      cartItems.push(itemObj);
      addToShoppingCart(itemObj);
    }

    // This will be called if the user clicks on one of the items in the basket.
    if (event.target.matches(".itemInTheCart"))
    {
      let clickedLiElement = event.target;
      // innerId value is stored as "innerId<number>". Extract the number from the expression.
      let clickedLiElementId = clickedLiElement.id.replace(/\D/g,'');

      // Get the object from the cartItems array, whose innerId equals innerId of the li element clicked by the user.
      for (let i = 0; i < cartItems.length; i++)
      {
        if (isEqual(clickedLiElementId, cartItems[i].innerId))
        {
          var item = cartItems[i];
          cartItems.splice(i, 1);
          break;
        }
      }

      removeFromShoppingCart(item);
    }

    // Checkout
    if (event.target.matches("#checkoutButton"))
    {
      const request = new XMLHttpRequest();
      request.open("POST", "../../orders/process_order/");
      request.setRequestHeader("Content-Type", "application/json");

      let csrfToken = getToken();
      request.setRequestHeader("x-csrftoken", csrfToken);

      request.send(JSON.stringify(cartItems));

      // After receiving response from the server, clear the localStorage and redirect the user to the order confirmation page.
      request.onload = () => {
        localStorage.removeItem("cartItems");
        localStorage.removeItem("innerId");
        window.location.replace(request.responseURL);
      };
    }

  }, false);


  // Before leaving the site save the basket value and innerId in localStorage.
  window.addEventListener("beforeunload", () => {
    localStorage.setItem("cartItems", JSON.stringify(cartItems));
    localStorage.setItem("innerId", innerId);
  });

});

function addToShoppingCart(item)
{
  let isSub = (item.itemType == "sub") ? "sub" : "";

  let itemDescription = document.createElement("li");
  // Assign each item class itemInTheCart in order to allow for item removal possibility.
  itemDescription.setAttribute("class", "itemInTheCart");
  // Assign each item an id that will look like innerId + number, for example "innerId1", "innerId23" etc.
  itemDescription.setAttribute("id", "innerId" + item.innerId);

  if (item.itemType == "pizza")
  {
    // Special pizza name formatting depending on the number of selected toppings.
    let pizzaName = (item.itemName == "topping1") ? "1 topping" : (item.itemName == "topping2") ? "2 toppings" : (item.itemName == "topping3") ? "3 toppings" : "cheese";
    itemDescription.innerHTML = `${item.itemSize} pizza with ${pizzaName} for ${item.itemPrice}$`;
  }
  else
  {
      itemDescription.innerHTML = `${item.itemSize} ${item.itemName} ${isSub} for ${item.itemPrice}$`;
  }

  totalPrice += Number(item.itemPrice);

  document.querySelector("#noItemsInTheCart").innerHTML = "";
  document.querySelector("#itemsInTheCart").appendChild(itemDescription);
  document.querySelector("#totalPrice").innerHTML = `Total price: <b>${totalPrice.toFixed(2)}</b>$`;
  document.querySelector("#checkoutButton").style.display = "block";
  document.querySelector("#shoppingCartInfo").style.display = "block";
}

function removeFromShoppingCart(item)
{
  // Get the li element that should be deleted.
  let liItemToRemove = document.querySelector("#innerId" + item.innerId);
  // Update basket's value.
  totalPrice -= Number(item.itemPrice);
  // Delete the element from the basket.
  document.querySelector("#itemsInTheCart").removeChild(liItemToRemove);
  document.querySelector("#totalPrice").innerHTML = `Total price: <b>${totalPrice.toFixed(2)}</b>$`;

  if (cartItems.length == 0)
  {
    document.querySelector("#noItemsInTheCart").innerHTML = "You have no items in your cart.";
    document.querySelector("#totalPrice").innerHTML = "";
    document.querySelector("#checkoutButton").style.display = "none";
    document.querySelector("#shoppingCartInfo").style.display = "none";
  }
}

function isEqual(idA, idB)
{
  return idA == idB;
}

function getToken()
{
    var name = "csrftoken";
    var cookieValue = null;
    if (document.cookie && document.cookie != '')
    {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++)
        {
            var cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) == (name + '='))
            {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
