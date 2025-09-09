# src/cocotbext/lin/config.py
import random

class LinConfig:
    """
    Configuration class for LIN protocol parameters.
    """
    def __init__(self, pid_width=6, max_data_length=8):
        self.pid_width = pid_width
        self.max_data_length = max_data_length

# Utility functions

def random_pid():
    """Generate a random LIN PID (6 bits)."""
    return random.randint(0, 0x3F)

def random_data():
    """Generate random LIN data bytes (1 to 8 bytes)."""
    length = random.randint(1, 8)
    data = [random.randint(0, 0xFF) for _ in range(length)]
    return length, data

