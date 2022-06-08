from typing import Union
import pandas as pd
from helper_function.file_process import *


class LocalFileDataSource:
    class Params:
        def __init__(self,
                     target_dir: str = '',
                     file_name_key_words: Union[list, tuple] = (),
                     file_formats: Union[list, tuple] = ()):
            self.target_dir = target_dir
            self.file_name_key_words = file_name_key_words
            self.file_formats = file_formats

    def __init__(self,
                 name: str = '',
                 path: str = None,
                 params: Params = None):
        self.name = name
        self.params = params
        self.path = path

        if self.path:
            self.format = self.path.split('.')[-1]
        else:
            self.path, self.format = self.update_path()

        self.data = None

    def update_path(self):
        p = scan_for_path(target_dir=self.params.target_dir,
                          file_name_key_words=self.params.file_name_key_words,
                          file_formats=self.params.file_formats
                          )

        if len(p) >= 1:
            self.path = p[0]
        else:
            self.path = None

        if self.path:
            self.format = self.path.split('.')[-1]
        else:
            self.format = None

        return self.path, self.format

    def load_data(self, **kwargs):
        if not self.path or self.format:
            self.update_path()

        if self.path and self.format:
            if self.format == 'csv':
                try:
                    self.data = pd.read_csv(self.path, index_col=False, **kwargs)
                except TypeError:
                    print('%s读取csv文件数据参数有误，现忽略' % self.name)
                    print(kwargs)
                    self.data = pd.read_csv(self.path)
            elif self.format in ['xlsx', 'xlsm', 'xls']:
                try:
                    self.data = pd.read_excel(self.path, **kwargs)
                except TypeError:
                    print('%s读取excel文件数据参数有误，现忽略' % self.name)
                    print(kwargs)
                    self.data = pd.read_excel(self.path)

            elif self.format == 'msg':
                pass

            else:
                print('%s 未识别的文件类型 %s' % (self.name, self.format))
                self.data = None
        else:
            return None

        return self.data
