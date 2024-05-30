import requests

# Function to get user input for range and algorithm
def get_user_input():
    start = int(input("Enter the start of the range: "))
    end = int(input("Enter the end of the range: "))
    algorithm = input("Enter the algorithm (sieve, simple_division, wheel_factorization, atkin_sieve, sundaram_sieve): ")
    return start, end, algorithm

# Function to make a request to the server to generate primes
def make_request(start, end, algorithm):
    response = requests.get(f'http://127.0.0.1:5000/primes?start={start}&end={end}&algorithm={algorithm}')
    return response.json()

# Function to fetch and print logs from the server
def print_logs():
    logs = requests.get('http://127.0.0.1:5000/logs').json()
    print("\nExecution Logs:")
    for log in logs:
        print(f"ID: {log['id']}")
        print(f"Timestamp: {log['timestamp']}")
        print(f"Range: {log['range_start']} to {log['range_end']}")
        print(f"Algorithm: {log['algorithm']}")
        print(f"Number of Primes: {log['num_primes']}")
        print(f"Primes: {log['primes']}")
        print(f"Time Elapsed: {log['time_elapsed']} seconds")
        print("-" * 50)

if __name__ == "__main__":
    start, end, algorithm = get_user_input()  # Get user input
    result = make_request(start, end, algorithm)  # Make request to server
    
    print_logs()  # Print the logs
