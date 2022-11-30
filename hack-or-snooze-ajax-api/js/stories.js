"use strict";

// This is the global list of the stories, an instance of StoryList
let storyList;

/** Get and show stories when site first loads. */
async function getAndShowStoriesOnStart() {
  storyList = await StoryList.getStories();
  $storiesLoadingMsg.remove();

  putStoriesOnPage();
}

/**
 * A render method to render HTML for an individual Story instance
 * - story: an instance of Story
 * Returns the markup for the story.
 * Generates delete button only when on the favorites or myStories page
 * Generates favorites button
 */
function generateStoryMarkup(story, showTrash) {
  //console.debug("generateStoryMarkup", story);

  const hostName = story.getHostName();
  let trash = showTrash ? getDeleteButton(story.storyId) : "";
  let star = getStarHTML(story, currentUser);
  return $(`
      <li id="${story.storyId}">
      ${trash}
      ${star} 
        <a href="${story.url}" target="a_blank" class="story-link">
          ${story.title}
        </a>
        <small class="story-hostname">(${hostName})</small>
        <small class="story-author">by ${story.author}</small>
        <small class="story-user">posted by ${story.username}</small>
      </li>
    `);
}

// Gets list of stories from server, generates their HTML, and puts on page.
function putStoriesOnPage() {
  console.debug("putStoriesOnPage");
  const showTrash = false;
  $allStoriesList.empty();

  // loop through all of our stories and generate HTML for them
  for (let story of storyList.stories) {
    const $story = generateStoryMarkup(story, showTrash);
    $allStoriesList.append($story);
  }

  $allStoriesList.show();
}

// Submit button
document.getElementById("submitButton").addEventListener("click", handleSubmit);

// Function allows users to add new stories to the page with titles, authors, and url links
async function handleSubmit(event){
  event.preventDefault();

  let titleValue = document.getElementById("title").value;
  let authorValue = document.getElementById("author").value;
  let urlValue = document.getElementById("url").value;

  const newStory = {
    title: titleValue,
    author: authorValue,
    url: urlValue,
  };

  let user = localStorage;
  let createdStory = await storyList.addStory(user, newStory);

  location.reload();
}

// Function that lists the user's created stories
function putUserStoriesOnPage() {
  console.debug("putUserStoriesOnPage");
  const showTrash = true;

  $ownStories.empty();

  if (currentUser.ownStories.length === 0) {
    $ownStories.append("You haven't added any stories yet.");
  }
  else {
    for (let story of currentUser.ownStories) {
      let $story = generateStoryMarkup(story, showTrash);
      $ownStories.append($story);
    }
  }
  $ownStories.show();
}

// Creates the Star Button
function getStarHTML(story, user) {
  if (user) {
  const isFavorite = user?.isFavorite(story);
  const starType = isFavorite ? "fas" : "far";
  return `
      <span class="star">
        <i class="${starType} fa-star"></i>
      </span>`;}
  else {
    return "";
  }
}

// Put favorites on favorites page
function putFavoritesListOnPage() {
  console.debug("putFavoritesListOnPage");
  const showTrash = true;
  $favoritedStories.empty();

  if (currentUser.favorites.length === 0) {
    $favoritedStories.append("<h5>No favorites added!</h5>");
  } else {
    // loop through all of users favorites and generate HTML for them
    for (let story of currentUser.favorites) {
      const $story = generateStoryMarkup(story, showTrash);
      $favoritedStories.append($story);
    }
  }
  $favoritedStories.show();
}

// Handles Favorite and Unfavorite clicks
async function toggleFavorite(evt) {
  console.debug("toggleFavorite");

  const $tgt = $(evt.target);
  const $closestLi = $tgt.closest("li");
  const storyId = $closestLi.attr("id");
  const story = storyList.stories.find((s) => s.storyId === storyId);

  // see if the story is already a favorite and has a checked star
  if ($tgt.hasClass("fas")) {
    // If the story is already a favorite, uncheck the star and remove from favorites
    await currentUser.removeFavorite(story);
    $tgt.closest("i").toggleClass("fas far");
  } else {
    // If the story is not a favorite check the star and add it to favorites
    await currentUser.addFavorite(story);
    $tgt.closest("i").toggleClass("fas far");
  }
}
$storiesLists.on("click", ".star", toggleFavorite);


// Creates the delete button
function getDeleteButton() {
  return `<span class="trash">
    <i class="fas fa-trash"></i></span>`;
}

// Handles deleting a story
$ownStories.on("click", ".trash", deleteStory);
async function deleteStory(evt) {

  const $closestLi = $(evt.target).closest("li");
  const storyId = $closestLi.attr("id");

  await storyList.removeStory(currentUser, storyId);

  // re-generate story list
  await putUserStoriesOnPage();
}
