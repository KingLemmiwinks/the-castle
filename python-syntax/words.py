def print_upper_words(words):
    """Print each word on a seperate line with uppercase letters"""


    for word in words:
        print(word.upper())

def print_upper_words_2(words):
    """Print each word on a separate line with uppercase letters if the word starts with E or e"""

    for word in words:
        if word.startswith("e") or word.startswith("E"):
            print(word.upper())

def print_upper_words_3(words, must_start_with):
    """Print each word on a separate line with uppercase letters if the word starts with the letter given"""

    for word in words:
        for letter in must_start_with:
            if word.startswith(letter):
                print(word.upper())
                break