import pygame

pygame.init()
sound_dict = dict(không='khong.ogg', một='mot1.ogg', mốt='mot2.ogg', hai='hai.ogg', ba='ba.ogg', bốn='bon.ogg',
                  năm='nam.ogg', lăm='lam.ogg', sáu='sau.ogg', bảy='bay.ogg', tám='tam.ogg', chín='chin.ogg',
                  mươi='muoi2.ogg', mười='muoi1.ogg', nghìn='nghin.ogg', triệu='trieu.ogg', trăm='tram.ogg',
                  linh='linh.ogg', lẻ='le.ogg', tỷ='ty.ogg')
vn_digits_dict = {0: 'không', 1: 'một', -1: 'mốt', 2: 'hai', 3: 'ba', 4: 'bốn', 5: 'năm',
                  -5: 'lăm', 6: 'sáu', 7: 'bảy', 8: 'tám', 9: 'chín'}
power_of_1k_dict = {0: '', 1: ' nghìn', 2: ' triệu', 3: ' tỷ'}
power_of_1k_dict_eng = {0: '', 1: ' thousand', 2: ' million', 3: ' billion'}
digits_in_units = {0: '', 1: 'one', 2: 'two', 3: 'three', 4: 'four',5: 'five',
                6: 'six', 7: 'seven', 8: 'eight', 9: 'nine'}
digits_in_tens = {0: '', 1: 'ten', 2: 'twenty', 3: 'thirty', 4: 'forty',
                  5: 'fifty', 6: 'sixty', 7: 'seventy', 8: 'eighty', 9: 'ninety'}
patch_num = {'ten-one': 'eleven', 'ten-two': 'twelve', 'ten-three': 'thirteen',
             'ten-four': 'fourteen', 'ten-five': 'fifteen', 'ten-six': 'sixteen',
             'ten-seven': 'seventeen', 'ten-eight': 'eighteen', 'ten-nine': 'nineteen'}


# Check validity of input:
def raise_exceptions(n):
    if not isinstance(n, int):
        raise TypeError('Not a integer')
    if not n >= 0:
        raise ValueError('Not a positive integer')
    if n > 999999999999:
        raise OverflowError('Maximum value exceeded')


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
y = lambda u: u.replace('không trăm linh', '').replace('không trăm', '')

# South-North string converter
southside = lambda u: u.replace('linh', 'lẻ').replace('nghìn', 'ngàn')


def integer_to_vietnamese_numeral(n, region='north', activate_tts=False):
    raise_exceptions(n)
    if not isinstance(region, type(None)):
        if not isinstance(region, str):
            raise TypeError('Invalid region input type')
        elif not region in ('south', 'north'):
            raise ValueError('Invalid region')
    if activate_tts != None and not isinstance(activate_tts, bool):
        raise TypeError('Not a boolean')
    if n == 0:
        return "không"

    def process_nums_less_than_1k(n):
        if n == 0:
            return ''
        digit_list = []
        # Split the number into a list of digits
        for i in range(0, 3):
            digit_list.append(n % 10)
            n //= 10
        # Change to fit the
        if digit_list[0] == 1 and not digit_list[1] in [0, 1]:
            digit_list[0] = -1
        if digit_list[0] == 5 and digit_list[1] != 0:
            digit_list[0] = -5
        nume_list = [vn_digits_dict[i] for i in digit_list]
        op = '{} trăm {} mươi {}'.format(nume_list[-1], nume_list[-2], nume_list[-3])
        return fix_abnormal_combs(op)

    # Format each element in the lists
    vn_numerals_list = [process_nums_less_than_1k(i) for i in nums_less_than_1k]
    vn_numerals_list[-1] = y(vn_numerals_list[-1])
    for i in range(len(vn_numerals_list)):
        if vn_numerals_list[i]:
            vn_numerals_list[i] += power_of_1k_dict[i]
    vn_numerals_list.reverse()
    # Join the list into a string
    raw_result = ' '.join(vn_numerals_list).split()
    result = ' '.join(raw_result).strip()
    # Regional conversion
    if region == 'south':
        result = southside(result)
    # Play sound (if necessary)
    if activate_tts:
        for i in raw_result:
            sound = pygame.mixer.Sound('./vie/{}/{}'.format(region, sound_dict[i]))
            sound.play()
            pygame.time.delay(500)
            pygame.mixer.stop()
    return result


def integer_to_english_numeral(n,activate_tts = False):
    raise_exceptions(n)
    if n == 0:
        return "Zero"

    def process_num_eng(n):
        digit_lst = []
        for i in range(0,3):
            digit_lst.append(n % 10)
            n //= 10
        digit_lst.reverse()
        if digit_lst[0] != 0:
            digit_lst[0] = digits_in_units[digit_lst[0]] + " hundred"
        else:
            digit_lst[0] = ''
        def repl(x,y):
            for i in x:
                if i == digit_lst[y]:
                    digit_lst[y] = x[i]
            return digit_lst[y]
        digit_lst[1] = repl(digits_in_tens, 1)
        digit_lst[2] = repl(digits_in_units, 2)
        if digit_lst[1] and digit_lst[2]:
             digit_lst[2] = '-' + digit_lst[2]
        digit_lst[1:3] = [''.join(digit_lst[1:3])]
        for i in patch_num:
            digit_lst[1] = digit_lst[1].replace(i, patch_num[i])
        if not digit_lst[0] or not digit_lst[1]:
            output = ''.join(digit_lst)
        else:
            output = digit_lst[0] + ' and ' + digit_lst[1]
        return output.strip()

    nums_less_than_1k = num_splitting(n)
    eng_numerals_list = [process_num_eng(i) for i in nums_less_than_1k]
    for i in range(len(eng_numerals_list)):
        if eng_numerals_list[i]:
            eng_numerals_list[i] += power_of_1k_dict_eng[i]
    eng_numerals_list.reverse()
    if eng_numerals_list[-1]:
        eng_numerals_list[-1] = 'and {}'.format(eng_numerals_list[-1])
    result = ' '.join(eng_numerals_list)
    if 'thousand' in result:
        result = result.replace('billion', 'billion,').replace('million','million,')
    result = ' '.join(result.split()).strip()
    if activate_tts == True:
        value_for_tts = result.replace('-',' ').split()
        for i in value_for_tts:
            sound = pygame.mixer.Sound('./vie/{}/{}'.format(region, sound_dict[i]))
            sound.play()
            pygame.time.delay(500)
            pygame.mixer.stop()
    return result
