def number_calc(string_number):
    try:
        int_list = [int(x) for x in string_number]
        mult = int_list[0]
        for i in int_list[1:]:
            mult *= i
        return mult
    except:
        return str(ValueError('В строке пристутствует не число'))
