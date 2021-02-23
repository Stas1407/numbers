# import math
# import time
# from timeout import Timeout
# from ThreadWithReturn import ThreadWithReturn
# import threading
# import random
# from primesieve import Iterator
#
#
# def prime_generator(n):
#     it = Iterator()
#     primes = []
#
#     for i in range(0, n):
#         prime = it.next_prime()
#         primes.append(prime)
#
#     return primes
#
#
# smallprimeset = set(prime_generator(100000))
# _smallprimeset = 100000
#
# @Timeout(30)
# def is_prime(n, precision=30):
#     # http://en.wikipedia.org/wiki/Miller-Rabin_primality_test#Algorithm_and_running_time
#     try:
#         n = abs(int(n))
#     except ValueError:
#         print("Input must be a non-negative integer")
#     if n in [0, 1]:
#         return False
#     elif n in [2, 3, 5]:
#         return True
#     elif n % 2 == 0:
#         return False
#     elif n < _smallprimeset:
#         return n in smallprimeset
#
#     # Miller-Rabin primality test
#
#     d = n - 1
#     s = 0
#     while d % 2 == 0:
#         d //= 2
#         s += 1
#
#     for repeat in range(precision):
#         a = random.randrange(2, n - 2)
#         x = pow(a, d, n)
#
#         if x == 1 or x == n - 1: continue
#
#         for r in range(s - 1):
#             x = pow(x, 2, n)
#             if x == 1: return False
#             if x == n - 1: break
#         else:
#             return False
#     return True
#
#
# divisors_tab = []
# semiprime = False
#
# @Timeout(20)
# def get_divisors_ext(n):
#     global divisors_tab
#     global semiprime
#     i = 1
#     while i * i < n:
#         if n % i == 0:
#             d = n // i
#             divisors_tab.append(i)
#             divisors_tab.append(d)
#             if not semiprime:
#                 if is_prime(i) and is_prime(d):
#                     print("Liczba półpierwsza (Iloczyn {0} i {1})".format(i, d))
#                     semiprime = True
#
#         i += 1
#     divisors_tab = sorted(divisors_tab)
#     return True
#
# @Timeout(5)
# def is_palindromic(n):
#     n = list(str(n))
#     first_half = n[:len(n) // 2]
#     second_half = n[math.ceil(len(n) / 2):]
#     if first_half == list(reversed(second_half)):
#         return True
#     return False
#
# @Timeout(5)
# def is_square(n):
#     element = math.sqrt(n)
#     if math.floor(element) == math.ceil(element):
#         return True
#     return False
#
# @Timeout(5)
# def is_triangle(n):
#     delta = 1 - 4 * (-2 * n)
#     if delta < 0:
#         return False
#     x1 = (-1 - math.sqrt(delta)) / 2
#     x2 = (-1 + math.sqrt(delta)) / 2
#     if x1 >= 0 and math.ceil(x1) == math.floor(x1):
#         return True
#     elif x2 >= 0 and math.ceil(x2) == math.floor(x2):
#         return True
#     return False
#
# def get_divisors_check_semiprime(n):
#     print('Divisors: Start')
#     start_time = time.time()
#
#     try:
#         get_divisors_ext(n)
#     except TimeoutError:
#         print('Divisors: Timeout after {}'.format(time.time() - start_time))
#         global divisors_tab
#         divisors_tab = sorted(divisors_tab)
#         return False
#
#     print('Divisors: End after {}'.format(time.time() - start_time))
#     return True
#
# def check_primality(n):
#     print('Primarility: start')
#     start_time = time.time()
#
#     try:
#         if is_prime(n):
#             print("Liczba pierwsza")
#             print('Primarility: end after {}'.format(time.time() - start_time))
#             return {'prime': True, 'primality_timeout': False}
#         else:
#             print('Primarility: end after {}'.format(time.time() - start_time))
#             return {'prime': False, 'primality_timeout': False}
#     except TimeoutError:
#         print('Primarility: Timeout after {}'.format(time.time() - start_time))
#         return {'prime': False, 'primality_timeout': True}
#
#
# def check_additional(n):
#     print('Additional: start')
#     start_time = time.time()
#     taxicab_numbers = [2, 1729, 87539319, 6963472309248, 48988659276962496]
#     data = {'taxicab': False, 'palindromic': False, 'square': False, 'triangle': False}
#
#     if n in taxicab_numbers:
#         print("Liczba taksówkowa")
#         data['taxicab'] = True
#
#     try:
#         if is_palindromic(n):
#             print("Liczba palindromiczna")
#             data['palindromic'] = True
#
#         if is_square(n):
#             print("Liczba kwadratowa")
#             data['square'] = True
#
#         if is_triangle(n):
#             print("Liczba trójkątna")
#             data['triangle'] = True
#     except TimeoutError:
#         print('Additional: Timeout after {}'.format(time.time() - start_time))
#         data['additional_timeout'] = True
#         return data
#
#     print('Additional: end after {}'.format(time.time() - start_time))
#     return data
#
# def check_number(n):
#     if not n.isnumeric():
#         print('Podaj liczbę')
#         return False
#     if int(n) > 9999999999999999999999999:
#         print("Liczba jest za duża")
#         return False
#     if int(n) < 0:
#         print("Zła liczba")
#         return False
#     return True
#
# def main():
#     number = input("Type in the number to check: ")
#
#     if not check_number(number):
#         return
#     number = int(number)
#
#     divisors = ThreadWithReturn(target=get_divisors_check_semiprime, args=(number, ), name="divisors")
#     divisors.start()
#
#     # if number <= 9007199254740881:
#     primality = ThreadWithReturn(target=check_primality, args=(number,), name="primality")
#     primality.start()
#
#     # print("dec: ", int(number))
#     # print("hex: ", hex(number))
#     # print("oct: ", oct(number))
#     # print("bin: ", bin(number))
#
#     data = {'additional_timeout': False, 'primality_timeout': False}
#     data.update(check_additional(number))
#
#     data.update(primality.join())
#
#     global divisors_tab
#     global semiprime
#
#     if data['prime']:
#         for thread in threading.enumerate():
#             if thread.name == 'get_divisors_ext':
#                 time.sleep(0.001)
#                 thread.raise_exception()
#         result = True
#     else:
#         result = divisors.join()
#
#     if not result:
#         data['divisors_timeout'] = True
#     else:
#         data['divisors_timeout'] = False
#
#     data['semiprime'] = semiprime
#     data['divisors'] = divisors_tab
#
#     for thread in threading.enumerate():
#         time.sleep(0.001)
#         if thread.name != "MainThread" and "pydevd" not in thread.name:
#             thread.raise_exception()
#     print(data)
#     return True
#
#
# main()
from numbers import Number
n = input("Podaj liczbę: ")
number = Number()
data = number.run(n)
print(data)
