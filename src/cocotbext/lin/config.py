import random

def random_pid():
    return random.randint(0, 0x3F)

def random_data():
    length = random.randint(1, 8)
    data = [random.randint(0, 0xFF) for _ in range(length)]
    return length, data

