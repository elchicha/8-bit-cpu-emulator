from emulator.alu import ALU


def test_alu_add_simple():
    """ALU should add two numbers correctly"""
    alu = ALU()
    result = alu.add(0x05, 0x03)
    assert result == 0x08

def test_alu_add_overflow():
    """ALU should handle overflow correctly"""
    alu = ALU()
    result = alu.add(0xFF, 0x01)
    assert result == 0x00

def test_alu_add_sets_zero_flag():
    """ALU should set the zero flag when result is zero"""
    alu = ALU()
    alu.add(0x00, 0x00)
    assert alu.zero_flag == True

    alu.add(0x01, 0x01)
    assert alu.zero_flag == False

def test_alu_add_sets_negative_flag():
    """ALU should set the negative flag when result is negative"""
    alu = ALU()
    alu.add(0x00, 0xFF)
    assert alu.negative_flag == True

    alu.add(0x01, 0x01)
    assert alu.negative_flag == False

def test_alu_sub_simple():
    """ALU should subtract two numbers"""
    alu = ALU()
    result = alu.sub(0x0A, 0x03)
    assert result == 0x07

def test_alu_sub_with_underflow():
    """Subtraction underflow should wrap"""
    alu = ALU()
    result = alu.sub(0x00, 0x01)
    assert result == 0xFF


def test_alu_sub_sets_carry_flag_on_borrow():
    """Carry flag should be set when borrowing (a < b)"""
    alu = ALU()
    alu.sub(0x05, 0x0A)
    assert alu.carry_flag == True

    alu.sub(0x0A, 0x05)
    assert alu.carry_flag == False