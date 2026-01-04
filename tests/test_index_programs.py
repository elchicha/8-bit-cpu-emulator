from emulator.cpu import CPU

def test_loop_with_x_register():
    """
    Program: Loop 5 times using X as a counter
    Much cleaner than using accumulator!

    Assembly:
        LDX #$05    ; X = 5 (counter)

    LOOP:
        DEX         ; X--
        STX $0200   ; Store X to memory
        BNE LOOP    ; Branch to LOOP if X is not zero
    """
    cpu = CPU()

    # LDX #$05
    cpu.memory.write_byte(0x0000, 0xA2)
    cpu.memory.write_byte(0x0001, 0x05)
    # DEX
    cpu.memory.write_byte(0x0002, 0xCA)
    # STX $0200
    cpu.memory.write_byte(0x0003, 0x8E)
    cpu.memory.write_byte(0x0004, 0x00)
    cpu.memory.write_byte(0x0005, 0x02)
    # BNE (back to DEX at 0x0002)
    cpu.memory.write_byte(0x0006, 0xD0)
    cpu.memory.write_byte(0x0007, 0xFA)

    cpu.step()

    # Loop 5 times
    for expected in [4, 3, 2, 1, 0]:
        cpu.step()  # DEX
        cpu.step()  # STX
        cpu.step()  # BNE (last iteration doesn't branch)
        if expected > 0:
            assert cpu.program_counter.get() == 0x0002  # Branched back

    # Verify final state
    assert cpu.x_register.get() == 0x00
    assert cpu.memory.read_byte(0x0200) == 0x00
    assert cpu.program_counter.get() == 0x0008  # Exited loop


def test_register_shuffling():
    """
    Program: Move data between all registers
    Shows register transfer instructions

    Assembly:
        LDA #$42      ; A = 0x42
        TAX           ; X = A (0x42)
        TAY           ; Y = A (0x42)
        LDA #$00      ; A = 0
        TXA           ; A = X (0x42)
        LDA #$00      ; A = 0
        TYA           ; A = Y (0x42)
    """
    cpu = CPU()

    # LDA #$42
    cpu.memory.write_byte(0x0000, 0xA9)
    cpu.memory.write_byte(0x0001, 0x42)

    # TAX
    cpu.memory.write_byte(0x0002, 0xAA)

    # TAY
    cpu.memory.write_byte(0x0003, 0xA8)

    # LDA #$00
    cpu.memory.write_byte(0x0004, 0xA9)
    cpu.memory.write_byte(0x0005, 0x00)

    # TXA
    cpu.memory.write_byte(0x0006, 0x8A)

    # LDA #$00
    cpu.memory.write_byte(0x0007, 0xA9)
    cpu.memory.write_byte(0x0008, 0x00)

    # TYA
    cpu.memory.write_byte(0x0009, 0x98)

    # Execute
    cpu.step()  # LDA #$42
    assert cpu.accumulator.get() == 0x42

    cpu.step()  # TAX
    assert cpu.x_register.get() == 0x42

    cpu.step()  # TAY
    assert cpu.y_register.get() == 0x42

    cpu.step()  # LDA #$00
    assert cpu.accumulator.get() == 0x00

    cpu.step()  # TXA
    assert cpu.accumulator.get() == 0x42

    cpu.step()  # LDA #$00
    assert cpu.accumulator.get() == 0x00

    cpu.step()  # TYA
    assert cpu.accumulator.get() == 0x42