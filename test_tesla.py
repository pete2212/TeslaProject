import pytesla

#load pw info
cred = {}
f = open('pw_file.pw')
for l in f:
    l = l.split('=')
    cred[l[0].strip()] = l[1].strip()
print cred
mycar = pytesla.Connection(cred['user'], cred['pw']).vehicle('vin')
mycar.charge_state()
