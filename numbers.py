import math
import time
from timeout import Timeout
from ThreadWithReturn import ThreadWithReturn
import threading
import random
from primesieve import Iterator

class Number:
    """
    A class used to get information about a number

    ...

    Methods
    --------
    is_prime(n)
        Checks if number is prime and returns True/False
        After 30 seconds times out and raises exception
    is_palindromic(n)
        Checks if the number is palindromic (Reads the same from beginning and end)
        After 5 seconds times out and raises exception
    is_square(n)
        Checks if number is square (It's square root is integer)
        After 5 seconds times out and raises exception
    is_triangle(n)
        Checks if number is triangle
        After 5 seconds times out and raises exception
    get_divisors_check_semiprime(n)
        Gets all n's divisors and check if n is semiprime
    check_primality(n)
        Checks if number is prime and handles eventual exception
    get_number_systems(n)
        Gets n in binary, hexadecimal, octal and decimal systems
    check_additional(n)
        Gets additional information about n - is_square, is_triangle, is_palindromic, is taxicab
        and handles exceptions
    check_number(n)
        Checks if n is a positive integer
    run(n)
        Runs all of the above and returns all the information as a dictionary
    """

    def __init__(self):
        self._smallprimeset = set(self._prime_generator(10000))
        self._smallprimeset_n = 10000
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
            print("Input must be a non-negative integer")
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

    @Timeout(30)
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
            If the function has been running for 30 seconds

        Returns
        --------
        True
        """

        i = 1
        while i * i < n:
            if n % i == 0:
                d = n // i
                self.divisors_tab.append(i)
                self.divisors_tab.append(d)
                if not self.semiprime:
                    if self.is_prime(i) and self.is_prime(d):
                        print("Liczba półpierwsza (Iloczyn {0} i {1})".format(i, d))
                        self.semiprime = True
                        self.factors = [i, d]

            i += 1
        self.divisors_tab = sorted(self.divisors_tab)
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
            print(element)
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
        print('Divisors: Start')
        start_time = time.time()

        try:
            self._get_divisors_ext(n)
        except TimeoutError:
            print('Divisors: Timeout after {}'.format(time.time() - start_time))
            self.divisors_tab = sorted(self.divisors_tab)
            return False

        print('Divisors: End after {}'.format(time.time() - start_time))
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

        print('Primality: start')
        start_time = time.time()

        try:
            if self.is_prime(n):
                print("Liczba pierwsza")
                print('Primality: end after {}'.format(time.time() - start_time))
                return {'prime': True}
            else:
                print('Primality: end after {}'.format(time.time() - start_time))
                return {'prime': False}
        except TimeoutError:
            print('Primality: Timeout after {}'.format(time.time() - start_time))
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

        print("dec: ", dec_n)
        print("hex: ", hex_n)
        print("oct: ", oct_n)
        print("bin: ", bin_n)

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

        print('Additional: start')
        start_time = time.time()
        taxicab_numbers = [2, 1729, 87539319, 6963472309248, 48988659276962496]
        data = {'taxicab': False, 'palindromic': False, 'square': False, 'triangle': False}

        if n in taxicab_numbers:
            print("Liczba taksówkowa")
            data['taxicab'] = True

        try:
            if self.is_palindromic(n):
                print("Liczba palindromiczna")
                data['palindromic'] = True

            if self.is_triangle(n):
                print("Liczba trójkątna")
                data['triangle'] = True

            if self.is_square(n):
                print("Liczba kwadratowa")
                data['square'] = True

        except TimeoutError:
            print('Additional: Timeout after {}'.format(time.time() - start_time))
            data['additional_timeout'] = True
            return data

        print('Additional: end after {}'.format(time.time() - start_time))
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

        compare_light = "{:.6f}".format(n / LIGHT_SPEED)
        compare_sound = "{:.6f}".format(n / SOUND_SPEED)
        print("{0} m/s = {1} x prędkość światła".format(n, compare_light))
        print("{0} m/s = {1} x prędkość dźwięku".format(n, compare_sound))

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
            A list with numbers that n is a power of.
        """
        if n > 9999999999999999:
            return False

        data = []
        for i in range(2, 12):
            tmp = n
            is_power = True
            while tmp != 1:
                tmp /= i
                if math.ceil(tmp) != math.floor(tmp):
                    is_power = False
                    break
            if is_power:
                data.append(i)
        return data

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
            print('Podaj liczbę')
            return False
        # if int(n) > 9999999999999999999999999:
        #     print("Liczba jest za duża")
        #     return False
        if int(n) < 0:
            print("Zła liczba")
            return False
        return True

    def run(self, number):
        """Function that gets all of the information about the number

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

        data = {'timeouts': []}

        data.update(self.get_number_systems(number))
        data.update(self.compare_speed(number))
        data.update(self.check_additional(number))
        data['roots'] = self.check_roots(number)

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

        for thread in threading.enumerate():
            time.sleep(0.001)
            if thread.name != "MainThread" and "pydevd" not in thread.name:
                thread.raise_exception()

        return data
