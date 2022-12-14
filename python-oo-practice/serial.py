"""Python serial number generator."""

class SerialGenerator:
    """Machine to create unique incrementing serial numbers.
    
    >>> serial = SerialGenerator(start=100)

    >>> serial.generate()
    100

    >>> serial.generate()
    101

    >>> serial.generate()
    102

    >>> serial.reset()

    >>> serial.generate()
    100
    """

    def __init__(self, start=0):
        """Starts generating at the given start"""

        self.start = self.next = start

    def __repr__(self):
        """"Return the representation of the starting number"""
        
        return f"SerialGenerator start={self.start} next={self.next}"

    def generate(self):
        """Return the next sequential serial number"""

        self.next += 1
        return self.next - 1

    def reset(self):
        """Reset the number to the original start value"""

        self.next = self.start