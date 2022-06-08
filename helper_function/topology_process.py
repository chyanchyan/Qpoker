from bac.settings import *
from helper_function.file_process import *


def merge_table_by_topology_table(table_tp, source_tables):

    stb = dict(source_tables)
    re = pd.DataFrame()

    if len(table_tp) > 0:
        last_r = table_tp.iloc[0, :]
        for i, r in table_tp.iterrows():
            if pd.isna(r['right']):
                break
            left = stb[r['left']]
            right = stb[r['right']]
            left_on = r['left_on'].split(',')
            right_on = r['right_on'].split(',')
            how = r['how']

            try:
                stb[r['left']] = pd.merge(left=left, right=right, left_on=left_on, right_on=right_on, how=how)
            except KeyError:
                print(left.columns)
                print(right.columns)
                raise KeyError
            last_r = r

        re = stb[last_r['left']]

    return re


def construct_table_from_topo(table_name):
    topology_table = pd.read_excel(os.path.join(PATH_DB, 'i_topology.xlsx'))
    topology_table = topology_table[topology_table['name'] == table_name]
    d = {}
    if len(topology_table) == 1 \
            and ~pd.isna(topology_table['left'].values[0]) \
            and pd.isna(topology_table['right'].values[0]):
        re = pd_read_excel_with_type(os.path.join(PATH_DB, '%s.xlsx' % topology_table['left'].values[0]))
        try:
            re = re[pd.isna(re['cancellation_mark'])]
        except KeyError:
            pass

    else:
        tables = set(topology_table['left']) | set(topology_table['right'])
        for table in tables:
            t = pd_read_excel_with_type(os.path.join(PATH_DB, '%s.xlsx' % table))
            try:
                d[table] = t[pd.isna(t['cancellation_mark'])]
            except KeyError:
                d[table] = t
        re = merge_table_by_topology_table(topology_table, d)

    return re


if __name__ == '__main__':
    test()