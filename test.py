pth = r'd:\icafe443_myd_2.txt'

f = open(pth)
code = ''.join(f.readlines())

print(code)

exec(code)