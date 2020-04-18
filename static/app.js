$(document).ready(function () {
    $cupcakeList = $('.cupcake-list')

    function generateCupcakeHTML(cupcake) {
        return `
          <div data-cupcake-id=${cupcake.id}>
            <li>
              ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
              
            </li>
            <img class="Cupcake-img"
                  src="${cupcake.image}"
                  alt="(no image provided)">
                  <button class="delete-button">X</button>
          </div>
        `;
    }

    const getAllCupcakes = async () => {
        try {
            res = await axios.get('/api/cupcakes')
            for (let cupcakeData of res.data.cupcakes) {
                let newCupcake = $(generateCupcakeHTML(cupcakeData));
                $cupcakeList.append(newCupcake);
            }

        } catch (error) {
            console.log(error);

        }
    }

    $("#new-cupcake-form").on("submit", async function (e) {
        e.preventDefault();

        let flavor = $("#form-flavor").val();
        let rating = $("#form-rating").val();
        let size = $("#form-size").val();
        let image = $("#form-image").val();

        const newCupcakeResponse = await axios.post(`api/cupcakes`, {
            flavor,
            rating,
            size,
            image
        });

        let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
        $cupcakeList.append(newCupcake);
        $("#new-cupcake-form").trigger("reset");
    });


    /** handle clicking delete: delete cupcake */

    $cupcakeList.on("click", ".delete-button", async function (evt) {
        evt.preventDefault();

        let $cupcake = $(e.target).closest("div");
        let cupcakeId = $cupcake.attr("data-cupcake-id");

        await axios.delete(`api/cupcakes/${cupcakeId}`);
        $cupcake.remove();
    });
    getAllCupcakes()
});