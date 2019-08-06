digits_in_units = {0: '', 1: 'one', 2: 'two', 3: 'three', 4: 'four',5: 'five',
                6: 'six', 7: 'seven', 8: 'eight', 9: 'nine'}
digits_in_tens = {0: '', 1: 'ten', 2: 'twenty', 3: 'thirty', 4: 'forty',
                  5: 'fifty', 6: 'sixty', 7: 'seventy', 8: 'eighty', 9: 'ninety'}
patch_num = {'ten-one': 'eleven', 'ten-two': 'twelve', 'ten-three': 'thirteen',
             'ten-four': 'fourteen', 'ten-five': 'fifteen', 'ten-six': 'sixteen',
             'ten-seven': 'seventeen', 'ten-eight': 'eighteen', 'ten-nine': 'nineteen'}

             
def integer_to_english_numeral(n):
if not isinstance(n,int):
    raise TypeError('Not a integer')
if not n > 0:
    raise ValueError('Not a positive integer')
if n > 999999999999:
    raise OverflowError('Maximum value exceeded')

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
        print(digit_lst)
        if not digit_lst[0] or not digit_lst[1]:
            output = ''.join(digit_lst)
        else:
            output = digit_lst[0] + ' and ' + digit_lst[1]
        return output.strip()
