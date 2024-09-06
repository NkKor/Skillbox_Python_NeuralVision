def eratosthenus(n):
    primes = [True] * (n + 1)
    primes[0] = primes[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if primes[i]:
            for j in range(i * i, n + 1, i):
                primes[j] = False
    return [i for i, is_prime in enumerate(primes) if is_prime]

max_num = int(input("Введите максимальное число: "))

if max_num > 1000:
    print("Максимальное число не должно превышать 1000.")
    exit()

primes = eratosthenus(max_num)

print("Простые числа:")
for i in range(0, len(primes), 10):
    print(*primes[i:i + 10])
