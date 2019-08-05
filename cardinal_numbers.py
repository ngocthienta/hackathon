import pygame

pygame.init()
sound_basedir_north = './vie/north'
sound_dict = dict(không='khong.ogg', một='mot1.ogg', mốt='mot2.ogg', hai='hai.ogg', ba='ba.ogg', bốn='bon.ogg',
                  năm='nam.ogg', lăm='lam.ogg', sáu='sau.ogg', bảy='bay.ogg', tám='tam.ogg', chín='chin.ogg',
                  mươi='muoi2.ogg', mười='muoi1.ogg', nghìn='nghin.ogg', triệu='trieu.ogg', trăm='tram.ogg',
                  linh='linh.ogg', lẻ='le.ogg', tỷ='ty.ogg')
vn_digits_dict = {0: 'không', 1: 'một', -1: 'mốt', 2: 'hai', 3: 'ba', 4: 'bốn', 5: 'năm',
                  -5: 'lăm', 6: 'sáu', 7: 'bảy', 8: 'tám', 9: 'chín'}
power_of_1k_dict = {0: '', 1: ' nghìn', 2: ' triệu', 3: ' tỷ'}


# Fix abnormal combinations:
def fix_abnormal_combs(u):
    return u.replace('một mươi', 'mười').replace('không mươi', 'linh') \
        .replace('linh không', '').replace('mươi không', 'mươi') \
        .replace('mười không', 'mười')


# Fix other abnormal combinations for the leftmost digits:
y = lambda u: u.replace('không trăm linh', '').replace('không trăm', '')
# South-North string converter
southside = lambda u: u.replace('linh', 'lẻ').replace('nghìn', 'ngàn')


def integer_to_vietnamese_numeral(n, region='north', activate_tts=False):
    if not isinstance(n, int):
        raise TypeError('Not a integer')
    if not n > 0:
        raise ValueError('Not a positive integer')
    if n > 999999999999:
        raise OverflowError('Maximum value exceeded')
    if not isinstance(region, type(None)):
        if not isinstance(region, str):
            raise TypeError('Invalid region input type')
        elif not region in ('south', 'north'):
            raise ValueError('Invalid region')
    if activate_tts != None and not isinstance(activate_tts, bool):
        raise TypeError('Not a boolean')

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

    # Split the number into lists of numbers less than 1k
    nums_less_than_1k = []
    while n != 0:
        nums_less_than_1k.append(n % 1000)
        n //= 1000
    # Format each element in the lists
    vn_numerals_list = [process_nums_less_than_1k(i) for i in nums_less_than_1k]
    vn_numerals_list[0] = y(vn_numerals_list[0])
    for i in range(len(vn_numerals_list)):
        vn_numerals_list[i] += power_of_1k_dict[i]
    vn_numerals_list.reverse()
    # Join the list into a string
    result = ''
    for i in vn_numerals_list:
        if i:
            result += i + ' '
    # Regional conversion
    if region == 'south':
        result = southside(result)
    # Play sound (if necessary)
    if activate_tts:
        for i in result.split():
            sound = pygame.mixer.Sound('./vie/{}/{}'.format(region, sound_dict[i]))
            sound.play()
            pygame.time.delay(500)
            pygame.mixer.stop()
    return result.strip()


print(integer_to_vietnamese_numeral(405, region='north', activate_tts=True))
