def vowel_count(phrase):
    """Return frequency map of vowels, case-insensitive.

        >>> vowel_count('rithm school')
        {'i': 1, 'o': 2}
        
        >>> vowel_count('HOW ARE YOU? i am great!') 
        {'o': 2, 'a': 3, 'e': 2, 'u': 1, 'i': 1}
    """

    asum = 0
    esum = 0
    isum = 0
    osum = 0
    usum = 0

    for ltr in phrase:
        formatted_letter = ltr.lower()
        if formatted_letter == 'a':
            asum += 1
        elif formatted_letter == 'e':
            esum += 1
        elif formatted_letter == 'i':
            isum += 1
        elif formatted_letter == 'o':
            osum += 1
        elif formatted_letter == 'u':
            usum += 1

    if asum != 0:
        print(f"a: {asum}")

    if esum != 0:
        print(f"e: {esum}")

    if isum != 0:
        print(f"i: {isum}")

    if osum != 0:
        print(f"o: {osum}")
        
    if usum != 0:
        print(f"u: {usum}")
