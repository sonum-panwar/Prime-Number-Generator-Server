from abc import ABC, abstractmethod
import sqlite3  
from datetime import datetime  
import json  

# Abstract base class for Prime Generators
class PrimeGenerator(ABC):
    @abstractmethod
    def generate(self, start, end):
        pass

# Sieve of Eratosthenes algorithm for prime generation
class SieveOfEratosthenes(PrimeGenerator):
    def generate(self, start, end):
        if start > end:
            return []
        sieve = [True] * (end + 1)  # Boolean array to mark primes
        sieve[0] = sieve[1] = False  # 0 and 1 are not prime numbers
        p = 2
        while (p * p <= end):
            if sieve[p]:
                for i in range(p * p, end + 1, p):
                    sieve[i] = False  # Mark multiples of p as non-prime
            p += 1
        return [p for p in range(start, end + 1) if sieve[p]]

# Simple division method for prime generation
class SimpleDivision(PrimeGenerator):
    def generate(self, start, end):
        def is_prime(n):
            if n <= 1:
                return False
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    return False
            return True

        return [n for n in range(start, end + 1) if is_prime(n)]

# Wheel factorization method for prime generation
class WheelFactorization(PrimeGenerator):
    def generate(self, start, end):
        def is_prime(n):
            if n <= 1:
                return False
            if n in (2, 3, 5):
                return True
            if n % 2 == 0 or n % 3 == 0 or n % 5 == 0:
                return False
            i = 7
            w = 4
            while i * i <= n:
                if n % i == 0:
                    return False
                i += w
                w = 6 - w
            return True

        return [n for n in range(start, end + 1) if is_prime(n)]

# Sieve of Atkin algorithm for prime generation
class AtkinSieve(PrimeGenerator):
    def generate(self, start, end):
        if start > end:
            return []
        sieve = [False] * (end + 1)
        for x in range(1, int(end**0.5) + 1):
            for y in range(1, int(end**0.5) + 1):
                n = 4*x**2 + y**2
                if n <= end and n % 12 in (1, 5):
                    sieve[n] = not sieve[n]
                n = 3*x**2 + y**2
                if n <= end and n % 12 == 7:
                    sieve[n] = not sieve[n]
                n = 3*x**2 - y**2
                if x > y and n <= end and n % 12 == 11:
                    sieve[n] = not sieve[n]
        for n in range(5, int(end**0.5) + 1):
            if sieve[n]:
                for k in range(n**2, end + 1, n**2):
                    sieve[k] = False
        sieve[2] = sieve[3] = True
        return [x for x in range(start, end + 1) if sieve[x]]

# Sieve of Sundaram algorithm for prime generation
class SundaramSieve(PrimeGenerator):
    def generate(self, start, end):
        if start > end:
            return []
        n = (end - 1) // 2
        sieve = [True] * (n + 1)
        for i in range(1, n + 1):
            j = i
            while i + j + 2*i*j <= n:
                sieve[i + j + 2*i*j] = False
                j += 1
        primes = [2] + [2*i + 1 for i in range(1, n + 1) if sieve[i]]
        return [p for p in primes if p >= start]

# Class to log prime generation details into the database
class PrimeLogger:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def log(self, range_start, range_end, time_elapsed, algorithm, num_primes, primes):
        cursor = self.db_conn.cursor()
        cursor.execute('''
        INSERT INTO logs (timestamp, range_start, range_end, time_elapsed, algorithm, num_primes, primes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), range_start, range_end, time_elapsed, algorithm, num_primes, json.dumps(primes)))
        self.db_conn.commit()

# Function to initialize the database 
def init_db():
    conn = sqlite3.connect('prime.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        range_start INTEGER,
        range_end INTEGER,
        time_elapsed REAL,
        algorithm TEXT,
        num_primes INTEGER,
        primes TEXT
    )
    ''')
    conn.commit()
    return conn

db_conn = init_db()  # Initialize the database connection
prime_logger = PrimeLogger(db_conn)  

