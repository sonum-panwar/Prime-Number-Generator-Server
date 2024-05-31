from flask import Flask, request, jsonify
import time
import json
from prime_generator import (SieveOfEratosthenes, SimpleDivision, WheelFactorization, AtkinSieve, SundaramSieve, db_conn, prime_logger)

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Dictionary mapping algorithm names to their respective classes
algorithms = {
    'sieve': SieveOfEratosthenes(),
    'simple_division': SimpleDivision(),
    'wheel_factorization': WheelFactorization(),
    'atkin_sieve': AtkinSieve(),
    'sundaram_sieve': SundaramSieve()
}

def primes_algorithm(start, end, algorithm):
    return algorithms.get(algorithm, SieveOfEratosthenes()).generate(start, end)

# Endpoint to generate numbers
@app.route('/primes', methods=['GET'])
def get_primes():
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))
    algorithm = request.args.get('algorithm')

    start_time = time.time()  # Record the start time
    primes = primes_algorithm(start, end, algorithm)
    end_time = time.time()  # Record the end time
    time_elapsed = end_time - start_time

    prime_logger.log(start, end, time_elapsed, algorithm, len(primes), primes)

    return jsonify({
        'primes': primes,
        'start': start,
        'end': end,
        'algorithm': algorithm,
        'time_elapsed': time_elapsed,
        'num_primes': len(primes)
    })

# Endpoint to retrieve logs
@app.route('/logs', methods=['GET'])
def get_logs():
    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM logs')
    rows = cursor.fetchall()

    logs = []
    for row in rows:
        log = {
            "id": row[0],
            "timestamp": row[1],
            "range_start": row[2],
            "range_end": row[3],
            "time_elapsed": row[4],
            "algorithm": row[5],
            "num_primes": row[6],
            "primes": json.loads(row[7])
        }
        logs.append(log)

    return jsonify(logs)

if __name__ == '__main__':
    app.run(debug=True)

