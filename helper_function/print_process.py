import sys
import time


def spinner(formal='|'):
    sys.stdout.flush()
    if formal == '|':
        res = '/'
    elif formal == '/':
        res = '-'
    elif formal == '-':
        res = '\\'
    elif formal == '\\':
        res = '|'
    else:
        res = '|'

    sys.stdout.write(res)
    return res


def spin(speed=0.3):
    if speed < 0.3:
        speed = 0.3
    re = '|'
    while True:
        re = spinner(re)
        time.sleep(speed)


if __name__ == '__main__':
    for i in range(5):
        print(i)
        time.sleep(1)