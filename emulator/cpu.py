class Register:
    """An 8-bit register for CPU operations"""

    def __init__(self):
        self._value = 0

    def get(self):
        """Get the current value of the register"""
        return self._value

    def set(self, value):
        """Set the value of the register to *value*"""
        self._value = value & 0xFF # Mask to ensure 8-bit value


class ALU:
    def __init__(self):
        self.zero_flag = False
        self.negative_flag = False
        self.carry_flag = False

    def add(self, a, b):
        """Add two numbers using the ALU"""
        result = a + b
        self.carry_flag = result > 0xFF
        result = result & 0xFF
        self.zero_flag = (result == 0x00)
        self.negative_flag = (result & 0x80) != 0
        return result

    def sub(self, a, b):
        """Subtract two numbers using the ALU"""
        result = a - b
        self.carry_flag = result < 0x00
        result = result & 0xFF
        self.zero_flag = (result == 0x00)
        self.negative_flag = (result & 0x80) != 0
        return result
