console.log("Let's get this party started!");

const $gifBody = $("#gif-body");
const $search = $("#search");

// Form Submission
$("form").on("submit", async function (evt) {
  evt.preventDefault();

  let searchTerm = $search.val();
  $search.val("");

  const response = await axios.get("https://api.giphy.com/v1/gifs/search", {
    params: {
      q: searchTerm,
      api_key: "MhAodEJIJxQMxW9XqxKjyXfNYdLoOIym",
    },
  });
  addGif(response.data);
});

// Add Gif
function addGif(res) {
  let numResults = res.data.length;
  if (numResults) {
    let randomIndex = Math.floor(Math.random() * numResults);
    let $newCol = $("<div>", { class: "col-md-4 col-12 mb-4" });
    let $newGif = $("<img>", {
      src: res.data[randomIndex].images.original.url,
      class: "w-100",
    });
    $newCol.append($newGif);
    $gifBody.append($newCol);
  }
}

// Remove Gif
$("#remove").on("click", function () {
  $gifBody.empty();
});
