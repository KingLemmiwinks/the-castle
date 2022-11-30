"use strict";

/******************************************************************************
 * Handling navbar clicks and updating navbar
 */

/** Show main list of all stories when click site name */
function navAllStories(evt) {
  hidePageComponents();
  putStoriesOnPage();
}

$body.on("click", "#nav-all", navAllStories);

/** Show login/signup on click on "login" */
function navLoginClick(evt) {
  hidePageComponents();
  $loginForm.show();
  $signupForm.show();
}
$navLogin.on("click", navLoginClick);

/** When a user first logins in, update the navbar to reflect that. */
function updateNavOnLogin() {
  $(".main-nav-links").show();
  $navLogin.hide();
  $navLogOut.show();
  $navUserProfile.text(`${currentUser.username}`).show();
}

/** Show story submit form on clicking story "submit" */
function navSubmitStoryClick(evt) {
  hidePageComponents();
  $allStoriesList.show();
  $submitForm.show();
}
$navSubmitStory.on("click", navSubmitStoryClick);

// Show favorites page 
function navFavoritesClick(evt) {
  hidePageComponents();
  putFavoritesListOnPage();
}
$body.on("click", "#nav-favorites", navFavoritesClick);



function navProfileClick(evt) {
  hidePageComponents();
  $userProfile.show();
  const dateString = currentUser.createdAt;
  const D = new Date(dateString);
  const formattedDate = (D.getMonth() + 1) + "/" + (D.getDate()) + "/" + (D.getFullYear());
  $("#profile-name").text(currentUser.name);
  $("#profile-username").text(currentUser.username);
  $("#profile-account-date").text(formattedDate);
}
$navUserProfile.on("click", navProfileClick);

function navMyStories(evt) {
  hidePageComponents();
  putUserStoriesOnPage();
  $ownStories.show();
}
$body.on("click", "#nav-my-stories", navMyStories);