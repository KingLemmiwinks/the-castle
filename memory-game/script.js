const gameContainer = document.getElementById("game");
var cardOne = null;
var cardTwo = null;

const COLORS = [
  "red",
  "blue",
  "green",
  "orange",
  "purple",
  "red",
  "blue",
  "green",
  "orange",
  "purple"
];

// here is a helper function to shuffle an array
// it returns the same array with values shuffled
// it is based on an algorithm called Fisher Yates if you want ot research more
function shuffle(array) {
  let counter = array.length;

  // While there are elements in the array
  while (counter > 0) {
    // Pick a random index
    let index = Math.floor(Math.random() * counter);

    // Decrease counter by 1
    counter--;

    // And swap the last element with it
    let temp = array[counter];
    array[counter] = array[index];
    array[index] = temp;
  }

  return array;
}

let shuffledColors = shuffle(COLORS);

// this function loops over the array of colors
// it creates a new div and gives it a class with the value of the color
// it also adds an event listener for a click for each card
function createDivsForColors(colorArray) {
  for (let c = 0; c < colorArray.length; c++) {
    const color = colorArray[c];
    // create a new div
    const newDiv = document.createElement("div");

    // give it a class attribute for the value we are looping over
    newDiv.classList.add(color);

    newDiv.id = color+c;

    // call a function handleCardClick when a div is clicked on
    newDiv.addEventListener("click", handleCardClick);

    // append the div to the element with an id of game
    gameContainer.append(newDiv);
  }
}

// TODO: Implement this function!
function handleCardClick(event) {
  // you can use event.target to see which element was clicked
  //console.log(event);
  //console.log("you just clicked", event.target);

  let div = document.getElementById(event.target.id);

  if (cardOne == null && cardTwo == null){
    cardOne = div;
    console.log("cardOne = " + cardOne.id);
  }
  else {
    if (div == cardOne){
      return;
    }
    cardTwo = div;
    console.log("cardTwo = " + cardTwo.id);
  }

    div.style.backgroundColor = event.target.className;

    if (cardOne != null && cardTwo != null){
      checkCards();
      
    }
}

function checkCards(){
  if (cardOne.className != cardTwo.className){
    document.body.style.pointerEvents = "none";
    setTimeout(whiteOut, 1000);
  }
  else{
    cardOne.style.pointerEvents = "none";
    cardTwo.style.pointerEvents = "none";
      cardOne = null;
      cardTwo = null;
  }  
}

function whiteOut(){
      cardOne.style.backgroundColor = "white";
      cardTwo.style.backgroundColor = "white";
      cardOne = null;
      cardTwo = null;
      document.body.style.pointerEvents = "initial";
}



// when the DOM loads
createDivsForColors(shuffledColors);

/* */