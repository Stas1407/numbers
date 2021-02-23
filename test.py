import math

def check_roots(n):
    if number > 9999999999999999:
        return False

    data = {}
    for i in range(2, 11):
        tmp = n
        is_power = True
        while tmp != 1:
            tmp /= i
            if math.ceil(tmp) != math.floor(tmp):
                is_power = False
                break
        if is_power:
            data[str(i)] = True
    return data


number = int(input())
print(check_roots(number))
