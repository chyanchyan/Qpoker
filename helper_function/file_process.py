import zipfile
import rarfile
from shutil import copy
from typing import Union
import os
import pandas as pd
from helper_function.number_process import *
from helper_function.string_process import *


def merge_path(org_pth, dst_pth, replace=False):
    for root, dirs, files in os.walk(org_pth):
        for d in dirs:
            tdr = os.path.join(dst_pth, d)
            if not os.path.exists(tdr) or replace:
                os.mkdir(tdr)
        for file in files:
            dr = root[len(org_pth):]
            opth = root + '\\' + file
            tdr = dst_pth + dr
            tpth = tdr + '\\' + file
            if not os.path.exists(tpth) or replace:
                copy(opth, tpth)
            else:
                pass


def rename(pwd: str, file_name=''):
    """压缩包内部文件有中文名, 解压后出现乱码，进行恢复"""

    path = f'{pwd}/{file_name}'
    if os.path.isdir(path):
        for file in os.scandir(path):
            rename(path, file.name)
    new_name = file_name.encode('cp437').decode('gbk')
    os.rename(path, f'{pwd}/{new_name}')


def unzip_unrar(file_path: str, replace_if_exist=False):
    sp = file_path.split('.')
    dir_name = '.'.join(sp[:-1])
    ext = sp[-1]

    try:
        if ext == 'zip':
            file = zipfile.ZipFile(file_path)
        elif ext == 'rar':
            file = rarfile.RarFile(file_path)
        else:
            print('目前不支持该压缩文件格式 %s' % ext)
            return

        # 检查是否存在, 并判断是否覆盖
        if os.path.exists(dir_name) and not replace_if_exist:
            return
        else:
            os.mkdir(dir_name)
            file.extractall(dir_name)
            file.close()

            # 递归修复编码
            rename(dir_name)
    except:
        print(f'{file_path} unzip\\rar fail')


def scan_for_path(target_dir: str,
                  file_name_key_words: Union[list, tuple] = (),
                  file_formats: Union[list, tuple] = (),
                  get: str = 'first',
                  key_word_match_way: Union[str, type(all), type(any)] = all
                  ) -> list:

    re = []

    if not os.path.isdir(target_dir):
        return []

    if type(key_word_match_way) == str and key_word_match_way[:4] == 'link':
        for fmt in file_formats:
            p = os.path.join(target_dir, '.'.join([key_word_match_way[4:].join(file_name_key_words), fmt]))
            if os.path.exists(p):
                return [p]
        return []

    for root, dirs, files in os.walk(target_dir):
        for f in files:
            flags = []
            f_ = str(f)

            if len(file_name_key_words) == 0:
                flags.append(get_ext(f) in file_formats or len(file_formats) == 0)
            else:
                for key_word in file_name_key_words:
                    flags.append(key_word in f_ and (get_ext(f) in file_formats or len(file_formats) == 0))
                    f_.replace(key_word, '')
            if key_word_match_way(flags):
                if get == 'first':
                    return [os.path.join(root, f)]
                else:
                    re.append(os.path.join(root, f))

    if get == 'last':
        return [re[-1]]
    elif is_int(get):
        return [re[int(get)]]
    else:
        return re


def pd_read_excel_with_type(path) -> pd.DataFrame:
    dtp = pd.read_excel(path, sheet_name='dt')
    dtp = zip(dtp['f'], dtp['pd_dt'])
    l_ = ['"%s": %s' % (item[0], item[1]) for item in dtp]
    s_ = '{' + ', '.join(l_) + '}'
    dtp = eval(s_)
    try:
        res = pd.read_excel(path, dtype=dtp)
    except ValueError:
        print()
        raise ValueError
    return res


def test():
    p = r'D:\sharepoint\Vision\数据库\dump\5060880773940789248-institution_account_detail-20210609170948'
    f = r'futureClearDetail_20210609175629.csv'
    rename(p, '')


def test2():
    p = r'D:\sharepoint\sys_project_manager\国联2期\_raw\202106'
    kw = ['assets', 'pool', '202104', 'out']
    fs = ['csv']
    print(scan_for_path(p, kw, fs, get='all', key_word_match_way='link_'))


if __name__ == '__main__':
    test2()