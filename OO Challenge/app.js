class Vehicle {
  constructor(make, model, year) {
    this.make = make;
    this.model = model;
    this.year = year;
  }
  honk() {
    return "Beep";
  }
  toString() {
    return `The vehicle is a ${this.make} ${this.model} from ${this.year}.`;
  }
}

class Car extends Vehicle {
  constructor(make, model, year) {
    super(make, model, year);
    this.numWheels = 4;
  }
}

class Motorcycle extends Vehicle {
  constructor(make, model, year) {
    super(make, model, year);
    this.numWheels = 2;
  }
  revEngine() {
    return "VROOM!!!";
  }
}

class Garage {
  constructor(capacity) {
    this.vehicles = [];
    this.capacity = capacity;
  }
  add(newVehicle) {
    if (!(newVehicle instanceof Vehicle)) {
      return "Only vehicles are allowed in here!";
    }
    if (this.vehicles.length >= this.capacity) {
      return "Sorry, we're full.";
    }
    this.vehicles.push(newVehicle);
    return "Vehicle added!";
  }
}

let myVehicle = new Vehicle("Chevrolet", "Sonic", 2016);
myVehicle.honk();
myVehicle.toString();

let myCar = new Car("Toyota", "Corolla", 2005);
myCar.toString();
myCar.honk();
myCar.numWheels;

let myMotorcycle = new Motorcycle("Honda", "Nighthawk", 2000);
myMotorcycle.honk();
myMotorcycle.revEngine();
myMotorcycle.numWheels;

let garage = new Garage(2);
garage.vehicles;
garage.add(new Car("Hyundai", "Elantra", 2015));
garage.vehicles;
garage.add("Taco");

garage.add(new Motorcycle("Honda", "Nighthawk", 2000));
garage.vehicles;

garage.add(new Motorcycle("Honda", "Nighthawk", 2001));
