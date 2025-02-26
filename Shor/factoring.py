import random
from order_finding import find_order

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# # for testing purposes
# def find_order(a, N):
#     for r in range(1, N):
#         if pow(a, r, N) == 1:
#             return r
#     return None

def isPrime(N):
    '''check if N is prime'''
    if N <= 1:
        return False
    if N <= 3:
        return True
    if N % 2 == 0 or N % 3 == 0:
        return False
    i = 5
    while i * i <= N:
        if N % i == 0 or N % (i + 2) == 0:
            return False
        i += 6
    return True

def powerOfPrime(N):
    '''check if n = p^k where k >= 2 if so return p'''
    b=2
    while (2**b) <= N:
        low = 1
        high = N
        while (high-low) >= 2:
            mid = (low + high)//2

            if mid**b < N+1:
                prev = mid**b
            else:
                prev = N+1

            if prev == N:
                return mid

            if prev < N:
                low = mid
            else:
                high = mid
        b=b+1
    return None



def shors_algorithm(N):
    '''assuming N is not a prime else returns None'''
    if N % 2 == 0:
        return 2
    
    p = powerOfPrime(N)
    if p is not None: return p
    if isPrime(N): return None
    
    # expected number of attempts = 2
    while True:
        a = random.randint(2, N - 1)
        a = 4
        gcd_value = gcd(a, N)
        
        if gcd_value > 1:
            return gcd_value

        r = find_order(a, N, epsilon=0.1)
        if r is None or r % 2 != 0:
            continue

        x = pow(a, r // 2, N)
        if x == N - 1:
            continue

        factor1 = gcd(x - 1, N)
        factor2 = gcd(x + 1, N)
        if factor1 > 1:
            return factor1
        if factor2 > 1:
            return factor2


print("Enter N: ", end="")
N = int(input())
factor = shors_algorithm(N)
print(f"A non-trivial factor of {N} is {factor}")
