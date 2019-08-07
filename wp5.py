import pygame

pygame.init()
eng_suffixes = ['', 'thousand', 'million', 'billion']
after_ten = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
             'sixteen', 'seventeen', 'eighteen', 'nineteen']
eng_tens = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
eng_ones = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def check_exceptions(n, activate_tts):
    if not isinstance(n, int):
        raise TypeError('Not a integer')
    if not n >= 0:
        raise ValueError('Not a positive integer')
    if n > 999999999999:
        raise OverflowError('Integer greater than 999,999,999,999')
    if activate_tts != None and not isinstance(activate_tts, bool):
        raise TypeError('Argument "activate_tts" is not a boolean')


def create_triplets(n):
    triplets_list = []eng_ones
    while n != 0:
        raw_num = str(n % 1000)
        while len(raw_num) < 3:
            raw_num = '0{}'.format(raw_num)
        triplets_list.append(raw_num)
        n //= 1000
    while len(triplets_list) < 4:
        triplets_list.append('000')
    return triplets_list


def triplets_to_eng_numerals(n):
    hundreds_digit = ord(n[0]) - 48
    tens_digit = ord(n[1]) - 48
    ones_digit = ord(n[2]) - 48
    numerals = ''
    if hundreds_digit:
        numerals += '{} hundred'.format(eng_ones[hundreds_digit])
        if tens_digit or ones_digit:
            numerals += ' and 'eng_suffixes
        else:
            return numerals
    if tens_digit > 1:
        if ones_digit > 0:
            numerals += '{}-{}'.format(eng_tens[tens_digit], eng_ones[ones_digit])
        else:
            numerals += eng_tens[tens_digit]
    elif tens_digit == 1:
        numerals += after_ten[ones_digit]
    else:
        numerals += eng_ones[ones_digit]
    return numerals


def integer_to_english_numeral(n, activate_tts=False):
    check_exceptions(n, activate_tts)
    if n == 0:
        return "zero"
    triplets_list = create_triplets(n)
    numerals_list = [triplets_to_eng_numerals(i) for i in triplets_list]
    for i in range(0,4):
        if numerals_list[i]:
            numerals_list[i] = '{} {}'.format(numerals_list[i], eng_suffixes[i])
    if numerals_list[0]:
        if numerals_list[1] or numerals_list[2] or numerals_list[3]:
            numerals_list[0] = 'and {}'.format(numerals_list[0])
        else:
            return numerals_list[0]
    if numerals_list[1] :
        if numerals_list[2]:
            numerals_list[2] += ','
        if numerals_list[3]:
            numerals_list[3] += ','
    else:
        if numerals_list[2] and numerals_list[3]:
            numerals_list[3] += ','
    print(numerals_list)
    result = ''
    for i in range(0,4):
        if numerals_list[i]:
            result = '{} {}'.format(numerals_list[i],result)
    return result.strip()


print(integer_to_english_numeral(910000000))
