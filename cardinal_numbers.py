import mutagen
import pygame

vn_suffixes = ['', 'nghìn', 'triệu', 'tỷ']
vn_tens = ['linh', 'mười', 'hai mươi', 'ba mươi', 'bốn mươi', 'năm mươi', 'sáu mươi',
           'bảy mươi', 'tám mươi', 'chín mươi']
vn_ones = ['không', 'một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín']
sound_dict = {'không': 'khong', 'một': 'mot1', 'mốt': 'mot2', 'hai': 'hai', 'ba': 'ba',
              'bốn': 'bon', 'năm': 'nam', 'lăm': 'lam', 'sáu': 'sau', 'bảy': 'bay',
              'tám': 'tam', 'chín': 'chin', 'mươi': 'muoi2', 'mười': 'muoi1', 'nghìn': 'nghin',
              'ngàn': 'ngan', 'triệu': 'trieu', 'trăm': 'tram', 'linh': 'linh', 'lẻ': 'le', 'tỷ': 'ty'}
eng_suffixes = ['', 'thousand', 'million', 'billion']
after_ten = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
             'sixteen', 'seventeen', 'eighteen', 'nineteen']
eng_tens = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
eng_ones = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def check_exceptions(n, activate_tts):
    """Check for exceptions and raise error messages."""
    if not isinstance(n, int):
        raise TypeError('Not a integer')
    if not n >= 0:
        raise ValueError('Not a positive integer')
    if n > 999999999999:
        raise OverflowError('Integer greater than 999,999,999,999')
    if activate_tts is not None and not isinstance(activate_tts, bool):
        raise TypeError('Argument "activate_tts" is not a boolean')


def create_triplets(n):
    """Divide non negative integer n into triplets and return a list."""
    triplets_list = []
    while n != 0:
        raw_num = str(n % 1000)
        while len(raw_num) < 3:
            raw_num = '0{}'.format(raw_num)
        triplets_list.append(raw_num)
        n //= 1000
    while len(triplets_list) < 4:
        triplets_list.append('000')
    return triplets_list


def triplet_to_vn_numeral(n):
    """Convert a triplet to VN numeral."""
    if n == '000':
        return ''
    hundreds_digit = ord(n[0]) - 48
    tens_digit = ord(n[1]) - 48
    ones_digit = ord(n[2]) - 48
    numeral = '{} trăm '.format(vn_ones[hundreds_digit])
    if not tens_digit and not ones_digit:
        return numeral.strip()
    numeral += '{} '.format(vn_tens[tens_digit])
    if ones_digit:
        if ones_digit == 1 and tens_digit > 1:
            numeral += 'mốt'
        elif ones_digit == 5 and tens_digit:
            numeral += 'lăm'
        else:
            numeral += vn_ones[ones_digit]
    return numeral.strip()


def text_to_speech(files_list, location):
    """Play sound files."""
    for i in files_list:
        address = './{}/{}.ogg'.format(location, i)
        audio_info = mutagen.File(address).info
        pygame.mixer.init(frequency=audio_info.sample_rate)
        pygame.mixer.music.load(address)
        pygame.mixer.music.play(0)
        pygame.time.delay(550)
        print(address)


def integer_to_vietnamese_numeral(n, side='north', activate_tts=False):
    """

    :param n:
    :param side: 
    :param activate_tts: a boolean
    :return:
    """
    check_exceptions(n, activate_tts)
    result = ''
    if n == 0:
        result = 'không'
    triplets_list = create_triplets(n)
    numerals_list = [triplet_to_vn_numeral(i) for i in triplets_list]
    print(numerals_list)
    for i in range(-1, -5, -1):
        if numerals_list[i]:
            numerals_list[i] = numerals_list[i].replace('không trăm linh', '').replace('không trăm', '')
            break
    for i in range(0, 4):
        if numerals_list[i]:
            result = '{} {} {}'.format(numerals_list[i], vn_suffixes[i], result)
    if side == 'south':
        result = result.replace('nghìn', 'ngàn').replace('linh', 'lẻ')
    if activate_tts:
        words_list = result.split()
        files_list = [sound_dict[i] for i in words_list]
        location = 'vie/{}'.format(side)
        text_to_speech(files_list, location)
    return result.strip()


def triplets_to_eng_numerals(n):
    """Convert a triplet to ENG numeral."""
    hundreds_digit = ord(n[0]) - 48
    tens_digit = ord(n[1]) - 48
    ones_digit = ord(n[2]) - 48
    numeral = ''
    if hundreds_digit:
        numeral += '{} hundred'.format(eng_ones[hundreds_digit])
        if tens_digit or ones_digit:
            numeral += ' and '
        else:
            return numeral
    if tens_digit > 1:
        if ones_digit > 0:
            numeral += '{}-{}'.format(eng_tens[tens_digit], eng_ones[ones_digit])
        else:
            numeral += eng_tens[tens_digit]
    elif tens_digit == 1:
        numeral += after_ten[ones_digit]
    else:
        numeral += eng_ones[ones_digit]
    return numeral


def integer_to_english_numeral(n, activate_tts=False):
    """
    
    :param n:
    :param activate_tts:
    :return:
    """
    check_exceptions(n, activate_tts)
    if n == 0:
        return "zero"
    triplets_list = create_triplets(n)
    numerals_list = [triplets_to_eng_numerals(i) for i in triplets_list]
    for i in range(0, 4):
        if numerals_list[i]:
            numerals_list[i] = '{} {}'.format(numerals_list[i], eng_suffixes[i])
    print(numerals_list)
    if numerals_list[0] and (numerals_list[1] or numerals_list[2] or numerals_list[3]):
        numerals_list[0] = 'and {}'.format(numerals_list[0])
    if numerals_list[1]:
        if numerals_list[2]:
            numerals_list[2] += ','
        if numerals_list[3]:
            numerals_list[3] += ','
    else:
        if numerals_list[2] and numerals_list[3]:
            numerals_list[3] += ','
    print(numerals_list)
    result = ''
    for i in range(0, 4):
        if numerals_list[i]:
            result = '{} {}'.format(numerals_list[i], result)
    if activate_tts:
        files_list = result.replace('-', ' ').replace(',', '').split()
        location = 'eng'
        text_to_speech(files_list, location)
    return result.strip()

print(integer_to_english_numeral(109999991203,True))
