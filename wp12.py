import pygame

pygame.init()
vn_suffixes = ['', 'nghìn', 'triệu', 'tỷ']
vn_tens = ['linh', 'mười', 'hai mươi', 'ba mươi', 'bốn mươi', 'năm mươi', 'sáu mươi',
           'bảy mươi', 'tám mươi', 'chín mươi']
vn_ones = ['không', 'một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín']
sound_dict = {'không': 'khong', 'một': 'mot1', 'mốt': 'mot2', 'hai': 'hai', 'ba': 'ba',
			  'bốn': 'bon', 'năm': 'nam', 'lăm': 'lam', 'sáu': 'sau', 'bảy': 'bay',
			  'tám': 'tam', 'chín': 'chin', 'mươi': 'muoi2', 'mười': 'muoi1',
			  'nghìn': 'nghin', 'triệu': 'trieu', 'trăm': 'tram','linh': 'linh',
			  'lẻ': 'le', 'tỷ': 'ty'}


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
    while len(triplets_list) < 4:
        triplets_list.append('000')
    return triplets_list


def triplets_to_vn_numerals(n):
	if n == '000':
		return ''
	hundreds_digit = ord(n[0]) - 48
	tens_digit = ord(n[1]) - 48
	ones_digit = ord(n[2]) - 48
	numerals = '{} trăm '.format(vn_ones[hundreds_digit])
	if not tens_digit and not ones_digit:
		return numerals.strip()
	numerals += '{} '.format(vn_tens[tens_digit])
	if ones_digit:
		if ones_digit == 1 and tens_digit > 1:
			numerals += 'mốt'
		elif ones_digit == 5 and tens_digit:
			numerals += 'lăm'
		else:
			numerals += vn_ones[ones_digit]
	return numerals.strip()


def text_to_speech(files_list, location, typ):
	for i in files_list:
		pygame.mixer.music.load('./{}/{}.{}'.format(location,i,typ))
		pygame.mixer.music.play(0)
		pygame.time.delay(540)


def integer_to_vietnamese_numeral(n, region='north', activate_tts=False):
	check_exceptions(n, activate_tts)
	if n == 0:
		return 'không'
	triplets_list = create_triplets(n)
	numerals_list = [triplets_to_vn_numerals(i) for i in triplets_list]
	result = ''
	print(numerals_list)
	for i in range(-1, -5, -1):
		if numerals_list[i]:
			numerals_list[i] = numerals_list[i].replace('không trăm linh', '').replace('không trăm', '')
			break
	for i in range(0,4):
		if numerals_list[i]:
			result = '{} {} {}'.format(numerals_list[i], vn_suffixes[i], result)
	if region == 'south':
		result = result.replace('nghìn', 'ngàn').replace('linh', 'lẻ')
	if activate_tts:
		words_list = result.split()
		files_list = [sound_dict[i] for i in words_list]
		location ='vie/{}'.format(region)
		typ = 'ogg'
		text_to_speech(files_list, location, typ)
	return result.strip()
print(integer_to_vietnamese_numeral(123478967534,region='north',activate_tts=True))
