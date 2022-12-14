"""Word Finder: finds random words from a dictionary."""

import random

class WordFinder:
    """Machine for finding random words from dictionary.
    
    >>> wf = WordFinder("words.txt")
    235886 words read

    >>> wf.random()
    """

    def __init__(self, path):
        """Reads the dictionary and prints the number of words in the file."""

        dict_file = open(path)

        self.words = self.parse(dict_file)
        print(self.words)

        print(f"{len(self.words)} words read")

    def parse(self, dict_file):
        """Parse dict_file -> list of words."""

        return [w.strip() for w in dict_file]

    def random(self):
        """Return random word."""

        return random.choice(self.words)


class SpecialWordFinder(WordFinder):
#     """Specialized WordFinder that excludes blank lines/comments.
    
    """WordFinder that excludes blank lines and comments
        >>> swf = SpecialWordFinder("subclass.txt")
        4 words read
        
        >>> swf.random()
        """

    def parse(self, dict_file):
        newlist = []
        for line in dict_file:
            if line.strip() and not line.startswith("#"):
                # if line is not empty and is not a comment, add to newlist[]
                newlist.append(line.strip())
        return newlist