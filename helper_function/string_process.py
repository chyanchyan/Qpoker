from bac.settings import *
import os
from itertools import combinations
from helper_function.number_process import *
from datetime import datetime as dt


def tag_replace(s, left_brace='{', right_brace='}', **kwargs):
    re = str(s)
    for key, value in kwargs:
        re = re.replace('%s%s%s' % (left_brace, str(key), right_brace), str(value))

    return re


class CMD:
    def __init__(self, cmd_str: str = ''):
        self.cmd = self.read_cmd(cmd_str)

    @staticmethod
    def read_cmd(cmd_str: str = None):
        res = {}

        if cmd_str and not pd.isna(cmd_str):
            # string pre work
            cmd_str = cmd_str.replace('；', ';')
            cmd_str = cmd_str.replace('，', ',')
            cmd_str = cmd_str.replace('’', "'")
            cmd_str = cmd_str.replace('’', "'")
            cmd_str = cmd_str.replace('“', '"')
            cmd_str = cmd_str.replace('”', '"')
            cmd_str = cmd_str.replace(' ', '')
            cmd_str = cmd_str.replace('\r', '')
            cmd_str = cmd_str.replace('\n', '')

            items = cmd_str.split(';')
            for item in items:
                pair = item.split('=')
                if len(pair) == 2:
                    res[pair[0]] = pair[1]
        else:
            pass

        return res

    def __getitem__(self, item):
        try:
            return self.cmd[item]
        except KeyError:
            return None


def get_file_name_and_ext(path: str):
    return os.path.basename(path).split('.')


def get_file_name(path: str):
    return get_file_name_and_ext(path)[0]


def get_ext(path: str):
    return get_file_name_and_ext(path)[1]


def get_file_folder(path: str):
    return os.path.dirname(path)


def next_file_name(s):
    print(s)

    dot_index = s.rfind('.')
    if dot_index > 0:
        full_filename = s[:dot_index]
        extension = s[dot_index:]
    else:
        full_filename = s
        extension = ''

    filename = full_filename
    current_file_index = 0

    if full_filename[-1] == ')':
        b_index = full_filename.rfind('(')
        if b_index > 0:
            brace_content = full_filename[b_index + 1: -1]
            if brace_content.isdigit():
                filename = full_filename[: b_index]
                current_file_index = int(brace_content) + 1

    return filename + '(' + str(current_file_index) + ')' + extension


def param_checking(d, key_params_list):
    flag = True
    for key_param in key_params_list:
        try:
            p = d[key_param]
        except KeyError:
            print('请在命令参数中添加 "%s" 信息' % key_param)
            flag = False

    return flag


def get_date_set(st, ed, mark, include_st=True, include_ed=True) -> list:

    """
    mark format: Y/M/D,[INT]

    :param st: starting date
    :param ed: ending date
    :param mark: mark string
    :param include_st: is including starting date
    :param include_ed: .. ending date
    :return: list of dates
    """
    re = []

    main_marks = mark.split(',')

    date_mark = main_marks[0].strip()

    if len(main_marks) == 2:
        choice_mark = main_marks[1].strip()
    else:
        choice_mark = ''

    year, month, day = date_mark.split('/')

    ys = []
    ms = []
    ds = []

    if is_int(year):
        ys = [int(year)]
    else:
        y_l = year[0]
        y_r = year[1:]
        if y_l == 'Y':
            ys = list(set([item.year for item in pd.date_range(st, ed)]))
            ys = eval('%s%s' % (ys, y_r))

    if is_int(month):
        ms = [int(month)]
    else:
        m_l = month[0]
        m_r = month[1:]
        if m_l == 'M':
            ms = list(set([item.month for item in pd.date_range(st, ed)]))
            ms = eval('%s%s' % (ms, m_r))

    if is_int(day):
        ds = [int(day)]
    else:
        d_l = day[0]
        d_r = day[1:]
        if d_l == 'D':
            ds = list(set([item for item in range(1, 32)]))
            ds = eval('%s%s' % (ds, d_r))

    all_dates = pd.date_range(st, ed, freq='d')
    all_dates = [item.to_pydatetime() for item in all_dates]
    for date in all_dates:
        if date.year not in ys:
            continue
        if date.month not in ms:
            continue
        if date.day not in ds:
            continue
        re.append(date)

    re = eval('%s%s' % ('re', choice_mark))

    if include_st:
        if re[0] != st:
            re.insert(0, st)
    if include_ed:
        if re[-1] != ed:
            re.append(ed)

    for i, item in enumerate(re):
        if not isinstance(item, type(dt.today())):
            print(item)
            re[i] = item.to_pydatetime

    return re


def get_notional_set(way_mark, init_notional_mark, times):
    re = []

    way = way_mark.strip()
    amount = init_notional_mark.strip()
    amount = float(amount)
    if way == 'dec':
        for i in range(times):
            re.append(-amount)
    elif way == 'asc':
        for i in range(times):
            re.append(amount)
    else:
        pass

    return re


def match_key_words(target_string, key_words, match_way=all):
    flags = []
    s = str(target_string)
    for kw in key_words:
        flags.append(kw in s)
        s.replace(kw, '')
    return match_way(flags)


def digital_to_chinese(digital):

    axi0 = ['角', '分']
    axi1 = ['拾', '佰', '仟']
    axi2 = ['圆', '万', '亿', '兆']

    char = {'1': '壹',
            '2': '贰',
            '3': '叁',
            '4': '肆',
            '5': '伍',
            '6': '陆',
            '7': '柒',
            '8': '捌',
            '9': '玖',
            '0': '零'}

    d_str = ('{:.%sf}' % str(len(axi0))).format(digital).replace('.', '')

    integer = d_str[:-2]
    decimal = d_str[-2:]

    integer = ''.join([char[x] for x in integer])
    decimal = ''.join([char[x] for x in decimal])

    integer = [integer[::-1][i * (len(axi1) + 1): (i + 1) * (len(axi1) + 1)][::-1] for i in range(len(axi2))]

    while '' in integer:
        integer.remove('')

    for index, item in enumerate(integer):
        integer[index] = [''.join(d + unit) for d, unit in
                            zip(
                                item,
                                list(
                                    axi1[::-1] + [axi2[index]]
                                )[-len(item):]
                            )
                            ]

    integer = integer[::-1]
    integer = [''.join(item) for item in integer]
    #print(integer)

    decimal = ''.join([d + unit for d, unit in zip(decimal, axi0)])

    re = ''.join(integer) + ''.join(decimal)

    for item in axi0:
        re = re.replace('零' + item, '零')

    for item in axi1:
        re = re.replace('零' + item, '零')

    while '零零' in re:
        re = re.replace('零零', '零')

    for item in axi2:
        if item != '圆':
            re = re.replace('零' + item, item)

    # 处理主轴元刻度和零的粘连问题
    re = re.replace('零圆', '圆')

    # 处理主轴刻度粘连问题
    for n in range(2, len(axi2)):
        combs = [item[::-1] for item in combinations(axi2[1:], n)]
        for comb in combs:
            comb = ''.join(comb)
            re = re.replace(comb, comb[0])

    # 处理最后一位为零的情况
    if re[-1] == '零':
        re = re[:-1]

    # 处理整数
    if digital % 1 == 0:
        re = re + '整'

    return re


def digital_to_chinese2(digital):
    d_ = digital
    str_digital = str(digital)
    chinese = {'1': '壹', '2': '贰', '3': '叁', '4': '肆', '5': '伍', '6': '陆', '7': '柒', '8': '捌', '9': '玖', '0': '零'}
    chinese2 = ['拾', '佰', '仟', '万', '亿', '厘', '分', '角']
    jiao = ''
    bs = str_digital.split('.')
    yuan = bs[0]
    if len(bs) > 1:
        jiao = bs[1]
    r_yuan = [i for i in reversed(yuan)]
    count = 0
    for i in range(len(yuan)):
        if i == 0:
            r_yuan[i] += '圆'
            continue
        r_yuan[i] += chinese2[count]
        count += 1
        if count == 4:
            count = 0
            chinese2[3] = '亿'

    s_jiao = [i for i in jiao][:3]  # 去掉小于厘之后的

    j_count = -1
    for i in range(len(s_jiao)):
        s_jiao[i] += chinese2[j_count]
        j_count -= 1
    last = [i for i in reversed(r_yuan)] + s_jiao

    last_str = ''.join(last)
    last_str = last_str.replace('0百', '0').replace('0十', '0').replace('000', '0').replace('00', '0').replace('0圆', '圆')
    for i in range(len(last_str)):
        digital = last_str[i]
        if digital in chinese:
            last_str = last_str.replace(digital, chinese[digital])

    last_str = last_str.replace('零角', '')
    last_str = last_str.replace('零分', '')
    for item in chinese2:
        last_str = last_str.replace('零' + item, '零')

    while '零零' in last_str:
        last_str = last_str.replace('零零', '零')

    last_str = last_str.replace('零圆', '圆')

    if d_ % 1 == 0:
        last_str += '整'
    else:
        pass

    return last_str


def print_line(s='-', length=100):
    print(s * length)


if __name__ == '__main__':
    ds = [
        1,
        1.0,
        1.01,
        1.1,
        10,
        11,
        12345,
        10000,
        10001,
        10101,
        100000000,
        100000001,
        100000000.01,
        100000000.1,
        100100010.1,
        556664200.82,
        100000000000
    ]
    for d in ds:
        print('{:,.2f}'.format(d), digital_to_chinese(d))
