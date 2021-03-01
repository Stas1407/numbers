import math
import json

def check_phone(n):
    if 999999999999 >= n >= 1000000000:
        data = []
        f = open('phone_numbers.json', )
        data = json.load(f)
        f.close()
        n = str(n)
        for o in data:
            if str(o['dial_code']).replace('+', "") in n[:3]:
                return o
    return {}

number = int(input())
print(check_phone(number))
