from flask import Flask, request, jsonify
import time
import json
from prime_generator import (sieve_of_eratosthenes, simple_division, wheel_factorization, atkin_sieve, sundaram_sieve, db_conn, log_execution)

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  

# Helper function to select the prime generation algorithm
def primes_algorithm(start, end, algorithm):
    if algorithm == 'sieve':
        return sieve_of_eratosthenes(start, end)
    elif algorithm == 'simple_division':
        return simple_division(start, end)
    elif algorithm == 'wheel_factorization':
        return wheel_factorization(start, end)
    elif algorithm == 'atkin_sieve':
        return atkin_sieve(start, end)
    elif algorithm == 'sundaram_sieve':
        return sundaram_sieve(start, end)
    else:
        return []

# Endpoint to generate primes
@app.route('/primes', methods=['GET'])
def get_primes():
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))
    algorithm = request.args.get('algorithm')

    start_time = time.time()  # Record the start time
    primes = primes_algorithm(start, end, algorithm)
    end_time = time.time()  # Record the end time
    time_elapsed = end_time - start_time  # Calculate the time elapsed

    log_execution(start, end, time_elapsed, algorithm, len(primes), primes)  # Log the execution details

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
    rows = cursor.fetchall()  # Fetch all log entries
    
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
    app.run(debug=True)  # Run the Flask web server
