import pygame

pygame.init()
suffixes = ['', 'thousand', 'million', 'billion']
after_ten = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
             'sixteen', 'seventeen', 'eighteen', 'nineteen']
tens = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
ones = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


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
    triplets_list = []
    while n != 0:
        raw_num = str(n % 1000)
        while len(raw_num) < 3:
            raw_num = '0{}'.format(raw_num)
        triplets_list.append(raw_num)
        n //= 1000
    return triplets_list


def triplets_to_eng_numerals(n):
    hundreds_digit = ord(n[0]) - 48
    tens_digit = ord(n[1]) - 48
    ones_digit = ord(n[2]) - 48
    numerals = ''
    if hundreds_digit != 0:
        numerals += '{} hundred '.format(ones[hundreds_digit])
        if tens_digit or ones_digit:
            numerals += 'and '
    else:
        pass
    if tens_digit >= 1:
        numerals += '{}-{}'.format(tens[tens_digit], ones[ones_digit])
    elif tens_digit == 1:
        numerals += after_ten[ones_digit]
    else:
        numerals += ones[ones_digit]
    return numerals


def integer_to_english_numeral(n, activate_tts=False):
    check_exceptions(n, activate_tts)
    triplets_list = create_triplets(n)
    numerals_list = [triplets_to_eng_numerals(i) for i in triplets_list]
    print(numerals_list)
    result = ''
    for i in range(len(numerals_list)):
        if not numerals_list[i]:
            pass
        else:
            result = '{} {} {}'.format(numerals_list[i], suffixes[i], result)

    return result


print(integer_to_english_numeral(901902000000))
