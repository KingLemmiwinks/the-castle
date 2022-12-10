def flip_case(phrase, to_swap):
    """Flip [to_swap] case each time it appears in phrase.

        >>> flip_case('Aaaahhh', 'a')
        'aAAAhhh'

        >>> flip_case('Aaaahhh', 'A')
        'aAAAhhh'

        >>> flip_case('Aaaahhh', 'h')
        'AaaaHHH'

    """
    formatted_phrase = ''
    for letter in phrase:
        if(letter == to_swap):
            if letter.isupper():
                letter = letter.lower()
            else:
                letter = letter.upper()
                
        formatted_phrase += letter

    return formatted_phrase