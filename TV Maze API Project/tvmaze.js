"use strict";

const $showsList = $("#shows-list");
const $episodesArea = $("#episodes-area");
const $searchForm = $("#search-form");
const $episodesList = $("#episodes-list");

const missingImage = "https://tinyurl.com/tv-missing";
const apiLink = "http://api.tvmaze.com/";

/** Given a search term, search for tv shows that match that query.
 *
 *  Returns (promise) array of show objects: [show, show, ...].
 *    Each show object should contain exactly: {id, name, summary, image}
 *    (if no image URL given by API, put in a default image URL)
 */

// ADD: Remove placeholder & make request to TVMaze search shows API.
async function getShowsByTerm(term) {
  let response = await axios({
    url: `http://api.tvmaze.com/search/shows?q=${term}`,
    method: "GET",
  });

  return response.data.map((result) => {
    let show = result.show;
    return {
      id: show.id,
      name: show.name,
      summary: show.summary,
      image: show.image ? show.image.medium : missingImage,
    };
  });
}

/** Given list of shows, create markup for each and to DOM */

function populateShows(shows) {
  $showsList.empty();

  for (let show of shows) {
    const $show = $(
      `<div data-show-id="${show.id}" class="Show col-md-12 col-lg-6 mb-4">
         <div class="media">
           <img 
              src="${show.image}" 
              alt="${show.name}" 
              class="w-25 mr-3">
           <div class="media-body">
             <h5 class="text-primary">${show.name}</h5>
             <div><small>${show.summary}</small></div>
             <button class="btn btn-secondary btn-sm Show-getEpisodes" data-show="${show.id}" >
               Episodes
             </button>
           </div>
         </div>  
       </div>
      `
    );

    $showsList.append($show);
  }

  // Defining onClicks after buttons have been rendered

  $(".Show-getEpisodes").on("click", async function (event) {
    var id = event.target.getAttribute("data-show");
    let episodes = await getEpisodesOfShow(id);
    populateEpisodes(episodes);
  });
}

/** Handle search form submission: get shows from API and display.
 *    Hide episodes area (that only gets shown if they ask for episodes)
 */

async function searchForShowAndDisplay() {
  const term = $("#search-query").val();
  const shows = await getShowsByTerm(term);

  $episodesArea.hide();
  populateShows(shows);
}

$searchForm.on("submit", async function (evt) {
  evt.preventDefault();
  await searchForShowAndDisplay();
});

/** Given a show ID, get from API and return (promise) array of episodes:
 *      { id, name, season, number }
 */

async function getEpisodesOfShow(id) {
  let response = await axios({
    url: `http://api.tvmaze.com/shows/${id}/episodes`,
    method: "GET",
  });

  let episodes = response.data.map(episode => ({
    id: episode.id,
    name: episode.name,
    season: episode.season,
    number: episode.number,
  }));
  return episodes;
}

/** Write a clear docstring for this function... */

function populateEpisodes(episodes) {
  let $episodesList = $("#episodes-list");
  $episodesList.empty();

  for (let episode of episodes) {
    const $item = $(
      `<li>
         ${episode.name}
         (season ${episode.season}, episode ${episode.number})
       </li>
      `);
    $episodesList.append($item);
  }
  $("#episodes-area").show();
}