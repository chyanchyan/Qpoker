from fnmatch import fnmatch
import pandas as pd
from datetime import datetime as dt
import os


def check_data_source(data_source_info, data_path):
    for key, value in data_source_info.items():
        for root, dirs, files in os.walk(data_path):
            for f in files:
                for file_format in value['format']:
                    if fnmatch(f, '*%s*.%s' % (value['identifier'], file_format)):
                        print(f)
                        break
                else:
                    continue
                break
            else:
                continue
            break
        else:
            continue


def pd_read_excel_with_type(path) -> pd.DataFrame:
    dtp = pd.read_excel(path, sheet_name='dt')
    dtp = zip(dtp['f'], dtp['pd_dt'])
    l_ = ['"%s": %s' % (item[0], item[1]) for item in dtp]
    s_ = '{' + ', '.join(l_) + '}'
    dtp = eval(s_)
    try:
        re = pd.read_excel(path, dtype=dtp)
    except ValueError:
        print()
        raise ValueError
    return re
