# Prime Number Generator

This project consists of a Flask web server that generates prime numbers within a specified range using various algorithms and logs the execution details in an SQLite database. The project includes three main components: a prime generator, a Flask server, and a script to interact with the server.

## Prime Generation Algorithms

The project supports the following prime generation algorithms:

1. Sieve of Eratosthenes (sieve)
2. Simple Division (simple_division)
3. Wheel Factorization (wheel_factorization)
4. Atkin Sieve (atkin_sieve)
5. Sundaram Sieve (sundaram_sieve)

## Endpoints

The Flask server provides the following endpoints:
- Generate Primes: /primes
  - Method: GET
  - Parameters:
    - start (int): Start of the range
    - end (int): End of the range
    - algorithm (string): Algorithm to use (sieve, simple_division, wheel_factorization, atkin_sieve, sundaram_sieve)
  - Response: JSON containing the list of prime numbers, range, algorithm, time elapsed, and number of primes

- Fetch Logs: /logs
  - Method: GET
  - Response: JSON containing the execution logs

## Database

- SQLite database (prime.db) with a single table logs.
- Table schema:
  - id: Auto-incremented primary key.
  - timestamp: Timestamp of the request.
  - range_start: Start of the range.
  - range_end: End of the range.
  - time_elapsed: Time taken to execute the request.
  - algorithm: Algorithm used.
  - num_primes: Number of primes found.
  - primes: List of primes (stored as JSON string).

