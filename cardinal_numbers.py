import pygame

pygame.init()
vn_sound_dict = dict(không='khong', một='mot1', mốt='mot2', hai='hai', ba='ba', bốn='bon',
                  năm='nam', lăm='lam', sáu='sau', bảy='bay', tám='tam', chín='chin',
                  mươi='muoi2', mười='muoi1', nghìn='nghin', triệu='trieu', trăm='tram',
                  linh='linh', lẻ='le', tỷ='ty')
vn_digits_in_units = {0: 'không', 1: 'một', -1: 'mốt', 2: 'hai', 3: 'ba', 4: 'bốn', 5: 'năm',
                  -5: 'lăm', 6: 'sáu', 7: 'bảy', 8: 'tám', 9: 'chín'}
vn_powers_of_1k = {0: '', 1: ' nghìn', 2: ' triệu', 3: ' tỷ'}
eng_powers_of_1k = {0: '', 1: ' thousand', 2: ' million', 3: ' billion'}
digits_in_units = {0: '', 1: 'one', 2: 'two', 3: 'three', 4: 'four',5: 'five',
                6: 'six', 7: 'seven', 8: 'eight', 9: 'nine'}
digits_in_tens = {0: '', 1: 'ten', 2: 'twenty', 3: 'thirty', 4: 'forty',
                  5: 'fifty', 6: 'sixty', 7: 'seventy', 8: 'eighty', 9: 'ninety'}
eng_nums_patch = {'ten-one': 'eleven', 'ten-two': 'twelve', 'ten-three': 'thirteen',
             'ten-four': 'fourteen', 'ten-five': 'fifteen', 'ten-six': 'sixteen',
             'ten-seven': 'seventeen', 'ten-eight': 'eighteen', 'ten-nine': 'nineteen'}


# Check validity of input:
def check_exceptions(n,activate_tts):
    if not isinstance(n, int):
        raise TypeError('Not a integer')
    if not n >= 0:
        raise ValueError('Not a positive integer')
    if n > 999999999999:
        raise OverflowError('Integer greater than 999,999,999,999')
    if activate_tts != None and not isinstance(activate_tts, bool):
        raise TypeError('Argument "activate_tts" is not a boolean')


# Split the number into lists of numbers less than 1k
def num_splitting(n):
    nums_less_than_1k = []
    while n != 0:
        nums_less_than_1k.append(n % 1000)
        n //= 1000
    return nums_less_than_1k


# Fix VN abnormal combinations:
def fix_abnormal_combs(u):
    return u.replace('một mươi', 'mười').replace('không mươi', 'linh') \
        .replace('linh không', '').replace('mươi không', 'mươi') \
        .replace('mười không', 'mười')


# Fix other VN abnormal combinations for the leftmost digits:
vn_further_repl = lambda u: u.replace('không trăm linh', '').replace('không trăm', '')

# South-North string converter
southside = lambda u: u.replace('linh', 'lẻ').replace('nghìn', 'ngàn')


def integer_to_vietnamese_numeral(n, region='north', activate_tts=False):
    check_exceptions(n,activate_tts)
    if not isinstance(region, type(None)):
        if not isinstance(region, str):
            raise TypeError('Argument "region" is not a string')
        elif not region in ('south', 'north'):
            raise ValueError('Argument "region" does not have a correct value')
    if n == 0:
        return "không"

    def vn_process_nums_less_than_1k(n):
        if n == 0:
            return ''
        digit_list = []
        # Split the number into a list of digits
        for i in range(0, 3):
            digit_list.append(n % 10)
            n //= 10
        # Change value according to the correct way of pronunciation
        if digit_list[0] == 1 and not digit_list[1] in [0, 1]:
            digit_list[0] = -1
        if digit_list[0] == 5 and digit_list[1] != 0:
            digit_list[0] = -5
        nume_list = [vn_digits_in_units[i] for i in digit_list]
        output = '{} trăm {} mươi {}'.format(nume_list[-1], nume_list[-2], nume_list[-3])
        return fix_abnormal_combs(output)

    # Convert numbers to numerals
    nums_less_than_1k = num_splitting(n)
    vn_numerals_list = [vn_process_nums_less_than_1k(i) for i in nums_less_than_1k]
    vn_numerals_list[-1] = vn_further_repl(vn_numerals_list[-1])
    for i in range(len(vn_numerals_list)):
        if vn_numerals_list[i]:
            vn_numerals_list[i] += vn_powers_of_1k[i]
    vn_numerals_list.reverse()
    # Join the numerals together
    raw_result = ' '.join(vn_numerals_list).split()
    result = ' '.join(raw_result).strip()
    # Regional conversion
    if region == 'south':
        result = southside(result)
    # Play sound
    if activate_tts:
        for i in raw_result:
            sound = pygame.mixer.Sound('./vie/{}/{}.ogg'.format(region, vn_sound_dict[i]))
            sound.play()
            pygame.time.delay(500)
            pygame.mixer.stop()
    return result


def integer_to_english_numeral(n,activate_tts = False):
    check_exceptions(n,activate_tts)
    if n == 0:
        return "zero"

    def eng_process_nums_less_than_1k(n):
        digit_list = []
        for i in range(0,3):
            digit_list.append(n % 10)
            n //= 10
        digit_list.reverse()
        if digit_list[0] != 0:
            digit_list[0] = digits_in_units[digit_list[0]] + " hundred"
        else:
            digit_list[0] = ''
        def repl(x,y):
            for i in x:
                if i == digit_list[y]:
                    digit_list[y] = x[i]
            return digit_list[y]
        digit_list[1] = repl(digits_in_tens, 1)
        digit_list[2] = repl(digits_in_units, 2)
        if digit_list[1] and digit_list[2]:
             digit_list[2] = '-' + digit_list[2]
        digit_list[1:3] = [''.join(digit_list[1:3])]
        for i in eng_nums_patch:
            digit_list[1] = digit_list[1].replace(i, eng_nums_patch[i])
        if not digit_list[0] or not digit_list[1]:
            output = ''.join(digit_list)
        else:
            output = digit_list[0] + ' and ' + digit_list[1]
        return output.strip()

    nums_less_than_1k = num_splitting(n)
    # Convert numbers to numerals
    eng_numerals_list = [eng_process_nums_less_than_1k(i) for i in nums_less_than_1k]
    for i in range(len(eng_numerals_list)):
        if eng_numerals_list[i]:
            eng_numerals_list[i] += eng_powers_of_1k[i]
    eng_numerals_list.reverse()
    # Add 'and'
    if eng_numerals_list[-1] and len(eng_numerals_list) != 1:
        eng_numerals_list[-1] = 'and {}'.format(eng_numerals_list[-1])
    # Add commas
    result = ' '.join(eng_numerals_list)
    if 'thousand' in result:
        result = result.replace('billion', 'billion,').replace('million','million,')
    # Join the numerals together
    result = ' '.join(result.split()).strip()
    # Play sound
    if activate_tts == True:
        value_for_tts = result.replace('-',' ').replace(',','').split()
        for i in value_for_tts:
            pygame.mixer.music.load('./eng/{}.mp3'.format(i))
            pygame.mixer.music.play(0)
            pygame.time.delay(800)
    return result
