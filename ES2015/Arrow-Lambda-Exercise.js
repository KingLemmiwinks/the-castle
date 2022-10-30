// function double(arr) {
//   return arr.map(function(val) {
//     return val * 2;
//   });
// }

const double = array => array.map(value => value * 2);


// function squareAndFindEvens(numbers){
//   var squares = numbers.map(function(num){
//     return num ** 2;
//   });
//   var evens = squares.filter(function(square){
//     return square % 2 === 0;
//   });
//   return evens;
// }

const squareAndFindEvens = numbers => numbers.map(value => value ** 2).filter(square => square % 2 === 0);