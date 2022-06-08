from itertools import chain
from datetime import datetime as dt
import shutil


def load_code(file_path):
    return [line.strip('\n') for line in open(file_path).readlines()]


def write_code(file_path, code_lines):
    f = open(file_path, 'w')
    for line in code_lines:
        f.write(line + '\n')
    f.close()


def format_code(code_lines):
    lines = [line.strip('\n').rstrip() for line in code_lines]
    lines = [line for line in filter(lambda x: len(x) != 0, lines)]
    return lines


def index_split_code_block(code_lines):
    if len(code_lines) > 0:
        sts = [i for i in range(len(code_lines)) if
               len(code_lines[i].strip()) > 0 and code_lines[i][0] != ' '
               ]

        return list(zip(sts, sts[1:] + [len(code_lines)]))
    else:
        return []


def split_code_block(code_lines):
    return [code_lines[sp[0]: sp[1]] for sp in index_split_code_block(code_lines)]


def locate_func(code_lines, block_type, block_name):
    block_loc = index_split_code_block(code_lines=code_lines)
    blocks = split_code_block(code_lines=code_lines)
    for block_index, block in enumerate(blocks):
        if block[0][:len(block_type) + len(block_name) + 2] == '%s %s:' % (block_type, block_name) or \
                block[0][:len(block_type) + len(block_name) + 2] == '%s %s(' % (block_type, block_name):
            return block, block_loc[block_index], block_index


def add_line_to_block(block, line):
    for k in block.__reversed__():
        if k.strip() != '':
            block.insert(block.index(k) + 1, line)
            break
    return block


def get_col_string(col_name, col_type, col_args=(), **kwargs):
    col_args = ', '.join(col_args)
    col_kwargs = ', '.join(['%s=%s' % (str(item[0]), str(item[1])) for item in kwargs.items()])
    res = '    %s = Column(%s, %s, %s)' % (col_name, col_type, col_args, col_kwargs)
    return res


def add_col_to_model(model_block, col_name, col_type, col_args=(), **kwargs):
    col_code_string = get_col_string(col_name=col_name, col_type=col_type, col_args=col_args, **kwargs)

    res = add_line_to_block(model_block, col_code_string)
    return res


def add_col_to_model_file_code_lines(code_lines, model_name, col_name, col_type, col_args=(), **kwargs):
    blocks = split_code_block(code_lines=code_lines)
    model_block, block_loc, model_code_block_index = \
        locate_func(code_lines=code_lines, block_type='class', block_name=model_name)
    model_block = add_col_to_model(model_block=model_block,
                                   col_name=col_name,
                                   col_type=col_type,
                                   col_args=col_args,
                                   **kwargs)
    blocks[model_code_block_index] = model_block
    res_lines = chain(*blocks)

    return res_lines


def add_col_to_model_file(file_path, model_name, col_name, col_type, update_comments='', col_args=(), **kwargs):
    back_up_path = r'.\\model_change_history\\models_%s_%s.py' % (dt.now().strftime('%Y%m%d_%H%M%S'), update_comments)
    shutil.copy(src=file_path, dst=back_up_path)

    res_lines = add_col_to_model_file_code_lines(code_lines=load_code(file_path),
                                                 model_name=model_name,
                                                 col_name=col_name,
                                                 col_type=col_type,
                                                 col_args=col_args,
                                                 **kwargs)

    write_code(file_path, res_lines)


def test():
    code_lines = open('models.py').readlines()
    block = locate_func(code_lines, 'class', 'Project')
    for line in block:
        print(line.strip('\n'))


def test_get_col_add_string():
    print(get_col_string(col_name='test_col', col_type='String(100)', col_args=['ForeignKey("test.id")'],
                         primary_key=True))


def test_add_col_to_model():
    code_lines = load_code('models.py')
    lines = add_col_to_model_file_code_lines(code_lines, 'Contact', 'test_add_col', 'String(100)', nullable=True)
    for line in lines:
        print(line)


def test_add_col_to_model_file():
    add_col_to_model_file('models.py', 'Contact', 'test_add_col', 'String(100)', 'test_add', nullable=True)


if __name__ == '__main__':
    test_get_col_add_string()

