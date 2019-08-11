import re

def neg_letter(string):
    """ Возвращает значение, содержатся ли сочетания минуса и буквы
     или двух минусов в строке"""

    if len(string.split('--')) > 1:
        return True

    for substring in string.split('-'):
        try:
            # первое число отрицательное
            if (len(substring)) == 0:
                continue

        except ValueError:
            return True
    return False


def number_calc(string):
    """Перемножает целые значения в строке с учетом отрицательных"""

    if neg_letter(string):
        return 'Недопустимое сочетание'

    string = re.sub('[^-\d]','', string)

    if len(string.split('-')) % 2 == 0:
        answer_sign = -1
    else:
        answer_sign = 1

    string = re.sub('[^\d]','', string)

    int_list = [int(x) for x in string]

    mult = int_list[0]
    for i in int_list[1:]:
        mult *= i

    return mult*answer_sign
