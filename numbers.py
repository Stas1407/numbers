import math
import time
from timeout import Timeout
from ThreadWithReturn import ThreadWithReturn
import threading
import random
from primesieve import Iterator
from bs4 import BeautifulSoup
import requests
import json

class Number:
    """
    A class used to get information about a number.

    ...

    Methods
    --------
    is_prime(n)
        Checks if number is prime and returns True/False.
        After 30 seconds times out and raises exception.
    is_palindromic(n)
        Checks if the number is palindromic (Reads the same from beginning and end).
        After 5 seconds times out and raises exception.
    is_square(n)
        Checks if number is square (It's square root is integer).
        After 5 seconds times out and raises exception.
    is_triangle(n)
        Checks if number is triangle.
        After 5 seconds times out and raises exception.
    get_divisors_check_semiprime(n)
        Gets all n's divisors and check if n is semiprime.
    check_primality(n)
        Checks if number is prime and handles eventual exception.
    get_number_systems(n)
        Gets n in binary, hexadecimal, octal and decimal systems.
    check_additional(n)
        Gets additional information about n - is_square, is_triangle, is_palindromic, is taxicab
        and handles exceptions.
    compare_speed(n)
        Compares n to the speed of light and sound.
    check_roots(n)
        Check if n is a power of any number in range <2;11>.
    check_bus(n)
        Check if n is a number of a bus. If yes return the list of stops of this bus (in Poland).
    check_year(n)
        Assumes that n is a year and checks if it's leap.
    check_phone(n)
        Assumes that n is a phone number and checks from which country is it.
    check_number(n)
        Checks if n is a positive integer.
    run(n)
        Runs all of the above and returns all the information as a dictionary.
    """

    def __init__(self):
        self._smallprimeset = set(self._prime_generator(10000))
        self._smallprimeset_n = 10000

        # dictionary comes from - https://gist.github.com/Goles/3196253
        f = open('phone_numbers.json', )
        self._phone_data = json.load(f)
        f.close()

        self.divisors_tab = []
        self.semiprime = False
        self.factors = []

    def _prime_generator(self, n):
        """Returns an array of first n prime numbers

        Parameters
        ----------
        n : int
            The number of prime numbers to return

        Returns
        ---------
        list
            A list of first n prime numbers
        """
        it = Iterator()
        primes = []

        for i in range(0, n):
            prime = it.next_prime()
            primes.append(prime)

        return primes

    @Timeout(10)
    def is_prime(self, n, precision=30):
        """Checks if number is prime

        Function uses Miller-Rabin primality test.
        Algorithm is not 100% accurate. It can return a composite number as a prime,
        but not the opposite.

        Parameters
        -----------
        n : int
            The number to check if it's prime
        precision : int, optional
            A number of repetitions of the algorithm. The higher the number the more precise is the result.

        Raises
        -------
        TimeoutError
            If the function has been running for 10 seconds
        ValueError
            If the number is not a positive integer

        Returns
        ---------
        True
            If the number is prime
        False
            If the number isn't prime
        """

        # http://en.wikipedia.org/wiki/Miller-Rabin_primality_test#Algorithm_and_running_time
        try:
            n = abs(int(n))
        except ValueError:
            pass

        if n in [0, 1]:
            return False
        elif n in [2, 3, 5]:
            return True
        elif n % 2 == 0:
            return False
        elif n < self._smallprimeset_n:
            return n in self._smallprimeset

        # Miller-Rabin primality test

        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1

        for repeat in range(precision):
            a = random.randrange(2, n - 2)
            x = pow(a, d, n)

            if x == 1 or x == n - 1: continue

            for r in range(s - 1):
                x = pow(x, 2, n)
                if x == 1: return False
                if x == n - 1: break
            else:
                return False
        return True

    @Timeout(20)
    def _get_divisors_ext(self, n):
        """Gets all n's divisors and checks if n is semiprime.
        It saves results in self.divisors_tab and self.semiprime

        Parameters
        -----------
        n : int
            The number to get it's divisors

        Raises
        -------
        TimeoutError
            If the function has been running for 20 seconds

        Returns
        --------
        True
        """

        i = 1
        while i * i <= n:
            if n % i == 0:
                d = n // i
                self.divisors_tab.append(i)
                self.divisors_tab.append(d)
                if not self.semiprime:
                    if self.is_prime(i) and self.is_prime(d):
                        self.semiprime = True
                        self.factors = [i, d]

            i += 1
        self.divisors_tab = list(set(sorted(self.divisors_tab)))
        return True

    @Timeout(5)
    def is_palindromic(self, n):
        """ Checks if number is palindromic.

        Parameters
        -----------
        n : int
            The number to check

        Raises
        ------
        TimeoutError
            If has been running for 5 seconds

        Return
        -------
        True
            If is palindromic
        False
            If isn't palindromic
        """

        n = list(str(n))
        first_half = n[:len(n) // 2]
        second_half = n[math.ceil(len(n) / 2):]
        if first_half == list(reversed(second_half)):
            return True
        return False

    @Timeout(5)
    def is_square(self, n):
        """ Checks if number is square.

        Parameters
        -----------
        n : int
            The number to check

        Raises
        ------
        TimeoutError
            If has been running for 5 seconds

        Return
        -------
        True
            If is square
        False
            If isn't square or if number is bigger than 999999999999999
        """

        if n > 999999999999999:
            return False

        element = math.sqrt(n)
        if math.floor(element) == math.ceil(element):
            return True
        return False

    @Timeout(5)
    def is_triangle(self, n):
        """ Checks if number is triangle.

        Parameters
        -----------
        n : int
            The number to check

        Raises
        ------
        TimeoutError
            If has been running for 5 seconds

        Return
        -------
        True
            If is triangle
        False
            If isn't triangle
        """

        delta = 1 - 4 * (-2 * n)
        if delta < 0:
            return False
        x1 = (-1 - math.sqrt(delta)) / 2
        x2 = (-1 + math.sqrt(delta)) / 2
        if x1 >= 0 and math.ceil(x1) == math.floor(x1):
            return True
        elif x2 >= 0 and math.ceil(x2) == math.floor(x2):
            return True
        return False

    def get_divisors_check_semiprime(self, n):
        """Gets n's divisors and checks if n is semiprime.
        It saves results in self.divisors_tab and self.semiprime

        Parameters
        -----------
        n : int
            A number to get it's divisors and check if it's semiprime

        Returns
        --------
        True
            If didn't time out
        False
            If timed out
        """

        try:
            self._get_divisors_ext(n)
        except TimeoutError:
            self.divisors_tab = sorted(self.divisors_tab)
            return False

        return True

    def check_primality(self, n):
        """Check if number n is prime

        Parameters
        ----------
        n: int
            Number to check if it's prime

        Returns
        --------
        dictionary
            A dictionary with keys:
                prime
                    True if number is prime
                primality_timeout
                    True if function timed out after 10 seconds
        """

        try:
            if self.is_prime(n):
                return {'prime': True}
            else:
                return {'prime': False}
        except TimeoutError:
            return {'prime': False, 'primality_timeout': True}

    def get_number_systems(self, n):
        """Gets n in binary, hexadecimal, octal and decimal systems.

        Parameters
        -----------
        n : int
            Number to convert

        Returns
        --------
        dictionary
            Dictionary with n in binary, hexadecimal, octal and decimal systems.
        """

        dec_n = int(n)
        hex_n = hex(n)
        oct_n = oct(n)
        bin_n = bin(n)

        return {"dec": dec_n, "hex": hex_n, "oct": oct_n, "bin": bin_n}

    def check_additional(self, n):
        """Check if number is taxicab, palindromic, square or triangle.

        Parameters
        -----------
        n : int
            Number to get information about

        Returns
        --------
        dictionary
            A dictionary containing keys: taxicab, palindromic, square, triangle.
            Values are True if number is given type or False if it isn't.
        """

        taxicab_numbers = [2, 1729, 87539319, 6963472309248, 48988659276962496]
        data = {'taxicab': False, 'palindromic': False, 'square': False, 'triangle': False}

        if n in taxicab_numbers:
            data['taxicab'] = True

        try:
            if self.is_palindromic(n):
                data['palindromic'] = True

            if self.is_triangle(n):
                data['triangle'] = True

            if self.is_square(n):
                data['square'] = True
        except TimeoutError:
            data['additional_timeout'] = True
            return data

        return data

    def compare_speed(self, n):
        """Compares n m/s to speed of light and speed of sound

        Parameters
        -----------
        n : int
            Number to compare

        Returns
        ---------
        dictionary
            A dictionary with keys: light, sound.
        """

        LIGHT_SPEED = 299792458
        SOUND_SPEED = 340

        compare_light = "{:.8f}".format(n / LIGHT_SPEED)
        compare_sound = "{:.8f}".format(n / SOUND_SPEED)

        return {'light': compare_light, 'sound': compare_sound}

    def check_roots(self, n):
        """Check if number is a power of any number in range <2;11>

        Parameters
        ----------
        n : int
            The number to check

        Returns
        --------
        False
            If n isn't a power of any of the numbers in range
        list
            A list of objects:
            {
                'number': A number that n is a power of
                'power': A power of the number
            }
        """
        
        if n > 9999999999999999:
            return False

        data = []
        for i in range(2, 12):
            tmp = n
            is_power = True
            count = 0
            while tmp != 1:
                count += 1
                tmp /= i
                if math.ceil(tmp) != math.floor(tmp):
                    is_power = False
                    break
            if is_power:
                data.append({'number': i, 'power': count})
        return data

    @Timeout(10)
    def check_bus(self, n):
        """Function checks if n is a bus number and
        if n is a bus number it returns all of it stops.

        Parameters
        ----------
        n : int
            Number to check

        Raises
        -------
        TimeoutError
            When is running for more than 10 seconds.

        Returns
        --------
        list
            A list with all stops of the bus (in Poland)
            If number is not a bus number it returns an empty list
        """

        BUS_URL = "https://rj.metropoliaztm.pl/rozklady/1-{}/"

        if n <= 998:
            url = BUS_URL.format(n)
            response = requests.get(url)
            data = response.text
            if "404 Wybrana strona nie istnieje" in data:
                return []

            soup = BeautifulSoup(data, features='html.parser')
            stops = soup.find_all('a', {'class': 'direction-list-group-item'})

            special_chars = [260, 262, 280, 321, 323, 211, 346, 377, 379]
            final_list = []
            for stop in stops[:math.ceil(len(stops) / 2)]:
                text = stop.text.replace("\n", "").replace(" ", "").replace("\t", "").replace(chr(160), "")

                i = 0
                shift = 0
                for char in text:
                    if (64 < ord(char) < 91 or ord(char) in special_chars) and i != 0:
                        text = text[:i + shift] + " " + text[i + shift:]
                        shift += 1
                    elif 47 < ord(char) < 58:
                        text = text[:i + shift]
                    i += 1

                final_list.append(text)

            return final_list
        else:
            return []

    def check_year(self, n):
        """Function assumes that number is a year and checks if it's a leap year.

        Parameters
        -----------
        n : int
            Number (year) to check

        Returns
        --------
        True
            If the year is leap
        False
            If the year isn't leap
        """

        if n > 0 and n % 4 == 0 and n % 100 != 0 or n % 400 == 0:
            return True
        return False

    def check_phone(self, n):
        """Function assumes that n is a phone number and checks from which country is it

        Parameters
        -----------
        n : int
            Number (phone number) to check

        Returns
        --------
        dictionary
            A dictionary with name, dial_code, code and flag of the country
        """

        if 999999999999999 >= n >= 1000000000:
            n = str(n)
            for o in self._phone_data:
                dial_code = str(o['dial_code']).replace('+', "")
                if dial_code in n[:len(dial_code)]:
                    return o
        return {}

    def check_number(self, n):
        """Checks if number is a positive integer

        Parameters
        -----------
        n : string
            Number to check (In string format)

        Returns
        --------
        True
            If number is a positive integer
        False
            If the number isn't a positive integer
        """

        if not n.isnumeric():
            print('You have to input a number')
            return False
        if int(n) < 0:
            print("Please type in a positive integer")
            return False
        return True

    def run(self, number):
        """Function that gets all of the information about the number.
        It runs all of the above functions in 5 different threads.
        Max execution time is 20 seconds.

        Parameters
        -----------
        number : int, str
            A number to get information about

        Returns
        -------
        dictionary
            A dictionary with all of the gathered data
        """

        if not self.check_number(str(number)):
            return
        number = int(number)

        divisors = ThreadWithReturn(target=self.get_divisors_check_semiprime, args=(number,), name="divisors")
        divisors.start()

        primality = ThreadWithReturn(target=self.check_primality, args=(number,), name="primality")
        primality.start()

        bus = ThreadWithReturn(target=self.check_bus, args=(number,), name="bus")
        bus.start()

        phone = ThreadWithReturn(target=self.check_phone, args=(number,), name="phone")
        phone.start()

        data = {'timeouts': []}

        data.update(self.get_number_systems(number))
        data.update(self.compare_speed(number))
        data.update(self.check_additional(number))
        data['roots'] = self.check_roots(number)
        data['year'] = self.check_year(number)

        if 'additional_timeout' in data:
            data['timeouts'].append('additional')
            del data['additional_timeout']

        data.update(primality.join())

        if 'primality_timeout' in data:
            data['timeouts'].append('primality')
            del data['additional_timeout']

        if data['prime']:
            for thread in threading.enumerate():
                if thread.name == '_get_divisors_ext':
                    time.sleep(0.001)
                    thread.raise_exception()
            result = True
        else:
            result = divisors.join()

        if not result:
            data['timeouts'].append('divisors')

        data['semiprime_factors'] = self.factors
        data['semiprime'] = self.semiprime
        data['divisors'] = self.divisors_tab

        data['phone'] = phone.join()

        try:
            data['bus'] = bus.join()
        except Exception:
            data['bus'] = []

        for thread in threading.enumerate():
            time.sleep(0.001)
            if thread.name != "MainThread" and "pydevd" not in thread.name:
                thread.raise_exception()

        return data
