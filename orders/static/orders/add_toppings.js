document.addEventListener("DOMContentLoaded", () => {

  document.addEventListener("click", function(event) {

    if (event.target.matches(".submitTopping"))
    {
      let pizzaId = event.target.dataset.pizza_id;
      let selectedToppings = event.target.form[0].selectedOptions;
      let toppingsIds = [];
      let toppingsNames = [];

      if (selectedToppings)
      {
        for (let i = 0; i < selectedToppings.length; i++)
        {
          toppingsIds.push(selectedToppings[i].value);
          toppingsNames.push(selectedToppings[i].dataset.name);
        }

        const request = new XMLHttpRequest();
        request.open("POST", "../../orders/add_toppings/");

        let data = new FormData();
        data.append("pizza_id", pizzaId);
        data.append("toppings_ids", JSON.stringify(toppingsIds));

        let csrfToken = getToken();
        request.setRequestHeader('x-csrftoken', csrfToken);

        request.send(data);

        request.onload = () => {
          if (JSON.parse(request.response).status === 200)
          {
            // Show the selected toppings in the toppings list
            let toppingsList = document.querySelector("#toppings" + pizzaId);
            for (let i = 0; i < toppingsNames.length; i++)
            {
              let newTopping = document.createElement("li");
              newTopping.innerHTML = toppingsNames[i];
              toppingsList.appendChild(newTopping);
            }

            document.querySelector("#toppingSelection" + pizzaId).style.display = "none";
          }
        };
      }
    }
  });
});

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
