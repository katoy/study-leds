import time

def calculate_pi_stream():
    """無限の円周率桁を生成するジェネレータ"""
    quotient, remainder, term, k, n, l = 1, 0, 1, 1, 3, 3
    decimal_point_shown = False

    while True:
        if 4 * quotient + remainder - term < n * term:
            yield n  # 確定した桁を出力

            # 小数点を1度だけ出力
            if not decimal_point_shown:
                yield "."
                decimal_point_shown = True

            quotient, remainder, term, k, n, l = update_for_next_digit(
                quotient, remainder, term, k, n, l
            )
        else:
            quotient, remainder, term, k, n, l = update_for_next_step(
                quotient, remainder, term, k, l
            )

def update_for_next_digit(quotient, remainder, term, k, n, l):
    """次の桁を確定するために変数を更新"""
    new_quotient = 10 * quotient
    new_remainder = 10 * (remainder - n * term)
    new_n = (10 * (3 * quotient + remainder)) // term - 10 * n
    return new_quotient, new_remainder, term, k, new_n, l

def update_for_next_step(quotient, remainder, term, k, l):
    """次のステップに進むために変数を更新"""
    new_quotient = quotient * k
    new_remainder = (2 * quotient + remainder) * l
    new_term = term * l
    new_k = k + 1
    new_n = (quotient * (7 * k + 2) + remainder * l) // (term * l)
    new_l = l + 2
    return new_quotient, new_remainder, new_term, new_k, new_n, new_l

def print_pi_stream(delay=0.1, space_every=10):
    """円周率の桁を指定された間隔で出力し、指定された桁数ごとにスペースを挿入"""
    digit_count = 0
    for digit in calculate_pi_stream():
        print(digit, end="", flush=True)
        digit_count += 1
        if digit_count == space_every:
            print(" ", end="", flush=True)  # 指定された桁数ごとにスペースを挿入
            digit_count = 0  # カウントをリセット
        time.sleep(delay)

# 円周率の桁を順次出力
print_pi_stream(delay=0)

