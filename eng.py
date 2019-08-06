eng_int_dict = {0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four',
                5: 'five',6: 'six', 7: 'seven', 8: 'eight',
                9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve',
                13: 'thirteen', 15: 'fifteen', 20: 'twenty',
                30: 'thirty', 50: 'fifty'}
repl_dict = {'oneteen' : 'eleven','twoteen' : 'twelve','fiveteen':'fiften','twoty':'twenty','fivety':'fifty'}
# def integer_to_english_numeral(n):
# if not isinstance(n,int):
#     raise TypeError('Not a integer')
# if not n > 0:
#     raise ValueError('Not a positive integer')
# if n > 999999999999:
#     raise OverflowError('Maximum value exceeded')
def process_num_eng(n):
    if n == 0:
        return ''
    digit_lst = []
    for i in range(0,3):
        digit_lst.append(n % 10)
        n //= 10
    print(digit_lst)
    nume_lst = []
    for i in digit_lst:
        if i == 0:
            nume_lst.append('')
        else:
            nume_lst.append(eng_int_dict[i])
    nume_lst.reverse()
    if nume_lst[0]:
        nume_lst[0] += ' hundred and'
    if nume_lst[1] == 'one':
        nume_lst[1] += 'teen'
        nume_lst[2] = ''
    elif nume_lst[1] == '':
        pass
    else:
        nume_lst[1] += 'ty'
    a = ' '.join(nume_lst).replace('ty ','ty-').strip()
    for i in repl_dict:
        if i in a:
            a = a.replace(i,repl_dict[i])
    return a

print(process_num_eng(400))
