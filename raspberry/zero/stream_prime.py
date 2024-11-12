import time

def is_prime(candidate, primes):
    """候補が素数かどうかを判定する関数"""
    return all(candidate % p != 0 for p in primes)

def prime_stream():
    """無限の素数を生成するジェネレータ"""
    primes = []  # 素数リスト
    candidate = 2  # 素数の候補

    while True:
        if is_prime(candidate, primes):
            primes.append(candidate)  # 素数リストに追加
            yield candidate  # 素数を出力
        candidate += 1  # 次の候補に進む

# 素数をストリームのように順次出力
def print_prime_stream(delay=0.5):
    """指定された間隔で素数を出力する関数"""
    for prime in prime_stream():
        print(prime, end=" ", flush=True)
        time.sleep(delay)

# 素数ストリームの出力を開始
print_prime_stream(0)

