def is_armstrong(n: int) -> bool:
    potential = str(n)
    power = len(potential)
    return n == sum(pow(int(num), power) for num in potential)
