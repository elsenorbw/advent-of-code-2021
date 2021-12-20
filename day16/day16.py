# --- Day 16: Packet Decoder ---

# As you leave the cave and reach open waters, you receive a transmission
# from the Elves back on the ship.

# The transmission was sent using the Buoyancy Interchange Transmission System
# (BITS), a method of packing numeric expressions into a binary sequence. Your
# submarine's computer has saved the transmission in hexadecimal
# (your puzzle input).

# The first step of decoding the message is to convert the hexadecimal
# representation into binary. Each character of hexadecimal corresponds to four
# bits of binary data:

# 0 = 0000
# 1 = 0001
# 2 = 0010
# 3 = 0011
# 4 = 0100
# 5 = 0101
# 6 = 0110
# 7 = 0111
# 8 = 1000
# 9 = 1001
# A = 1010
# B = 1011
# C = 1100
# D = 1101
# E = 1110
# F = 1111

# The BITS transmission contains a single packet at its outermost layer which
# itself contains many other packets. The hexadecimal representation of this
# packet might encode a few extra 0 bits at the end; these are not part of the
# transmission and should be ignored.

# Every packet begins with a standard header: the first three bits encode the
# packet version, and the next three bits encode the packet type ID. These two
# values are numbers; all numbers encoded in any packet are represented as
# binary with the most significant bit first. For example, a version encoded as
# the binary sequence 100 represents the number 4.

# Packets with type ID 4 represent a literal value. Literal value packets
# encode a single binary number. To do this, the binary number is padded with
# leading zeroes until its length is a multiple of four bits, and then it is
# broken into groups of four bits. Each group is prefixed by a 1 bit except the
# last group, which is prefixed by a 0 bit. These groups of five bits
# immediately follow the packet header. For example, the
# hexadecimal string D2FE28 becomes:

# 110100101111111000101000
# VVVTTTAAAAABBBBBCCCCC

# Below each bit is a label indicating its purpose:

#     The three bits labeled V (110) are the packet version, 6.
#     The three bits labeled T (100) are the packet type ID, 4, which means the packet is a literal value.
#     The five bits labeled A (10111) start with a 1 (not the last group, keep reading) and contain the first four bits of the number, 0111.
#     The five bits labeled B (11110) start with a 1 (not the last group, keep reading) and contain four more bits of the number, 1110.
#     The five bits labeled C (00101) start with a 0 (last group, end of packet) and contain the last four bits of the number, 0101.
#     The three unlabeled 0 bits at the end are extra due to the hexadecimal representation and should be ignored.

# So, this packet represents a literal value with binary representation
# 011111100101, which is 2021 in decimal.

# Every other type of packet (any packet with a type ID other than 4) represent
# an operator that performs some calculation on one or more sub-packets
# contained within. Right now, the specific operations aren't important; focus
# on parsing the hierarchy of sub-packets.

# An operator packet contains one or more packets. To indicate which subsequent
# binary data represents its sub-packets, an operator packet can use one of two
# modes indicated by the bit immediately after the packet header; this is
# called the length type ID:

#     If the length type ID is 0, then the next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet.
#     If the length type ID is 1, then the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet.

# Finally, after the length type ID bit and the 15-bit or 11-bit field, the sub-packets appear.

# For example, here is an operator packet (hexadecimal string 38006F45291200) with length type ID 0 that contains two sub-packets:

# 00111000000000000110111101000101001010010001001000000000
# VVVTTTILLLLLLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBBBBBB

#     The three bits labeled V (001) are the packet version, 1.
#     The three bits labeled T (110) are the packet type ID, 6, which means the packet is an operator.
#     The bit labeled I (0) is the length type ID, which indicates that the length is a 15-bit number representing the number of bits in the sub-packets.
#     The 15 bits labeled L (000000000011011) contain the length of the sub-packets in bits, 27.
#     The 11 bits labeled A contain the first sub-packet, a literal value representing the number 10.
#     The 16 bits labeled B contain the second sub-packet, a literal value representing the number 20.

# After reading 11 and 16 bits of sub-packet data, the total length indicated in L (27) is reached, and so parsing of this packet stops.

# As another example, here is an operator packet (hexadecimal string EE00D40C823060) with length type ID 1 that contains three sub-packets:

# 11101110000000001101010000001100100000100011000001100000
# VVVTTTILLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBCCCCCCCCCCC

#     The three bits labeled V (111) are the packet version, 7.
#     The three bits labeled T (011) are the packet type ID, 3, which means the packet is an operator.
#     The bit labeled I (1) is the length type ID, which indicates that the length is a 11-bit number representing the number of sub-packets.
#     The 11 bits labeled L (00000000011) contain the number of sub-packets, 3.
#     The 11 bits labeled A contain the first sub-packet, a literal value representing the number 1.
#     The 11 bits labeled B contain the second sub-packet, a literal value representing the number 2.
#     The 11 bits labeled C contain the third sub-packet, a literal value representing the number 3.

# After reading 3 complete sub-packets, the number of sub-packets indicated in L (3) is reached, and so parsing of this packet stops.

# For now, parse the hierarchy of the packets throughout the transmission and add up all of the version numbers.

# Here are a few more examples of hexadecimal-encoded transmissions:

#     8A004A801A8002F478 represents an operator packet (version 4) which contains an operator packet (version 1) which contains an operator packet (version 5) which contains a literal value (version 6); this packet has a version sum of 16.
#     620080001611562C8802118E34 represents an operator packet (version 3) which contains two sub-packets; each sub-packet is an operator packet that contains two literal values. This packet has a version sum of 12.
#     C0015000016115A2E0802F182340 has the same structure as the previous example, but the outermost packet uses a different length type ID. This packet has a version sum of 23.
#     A0016C880162017C3686B18A3D4780 is an operator packet that contains an operator packet that contains an operator packet that contains five literal values; it has a version sum of 31.

# Decode the structure of your hexadecimal-encoded BITS transmission; what do you get if you add up the version numbers in all packets?


from typing import List


class HexBinaryThingy:
    def __init__(self, bits=None) -> None:
        self.bits = []
        self.idx = 0
        if bits is not None:
            self.load_bits(bits)

    def load_hex_digits(self, hex: str):
        """
        Add the hex digits passed in into the bits list
        """
        bits_for_hexit = {
            "0": [0, 0, 0, 0],
            "1": [0, 0, 0, 1],
            "2": [0, 0, 1, 0],
            "3": [0, 0, 1, 1],
            "4": [0, 1, 0, 0],
            "5": [0, 1, 0, 1],
            "6": [0, 1, 1, 0],
            "7": [0, 1, 1, 1],
            "8": [1, 0, 0, 0],
            "9": [1, 0, 0, 1],
            "A": [1, 0, 1, 0],
            "B": [1, 0, 1, 1],
            "C": [1, 1, 0, 0],
            "D": [1, 1, 0, 1],
            "E": [1, 1, 1, 0],
            "F": [1, 1, 1, 1],
            "a": [1, 0, 1, 0],
            "b": [1, 0, 1, 1],
            "c": [1, 1, 0, 0],
            "d": [1, 1, 0, 1],
            "e": [1, 1, 1, 0],
            "f": [1, 1, 1, 1],
        }
        for this_hexit in hex:
            self.bits.extend(bits_for_hexit[this_hexit])

    def __repr__(self) -> str:
        result = f"HexBinaryThing<total_bits={len(self.bits)}, idx={self.idx}, remaining_bits={len(self.bits) - self.idx}>"
        return result

    def load_bits(self, bits: List[int]):
        """
        Add the bits to the array
        """
        self.bits.extend(bits)

    def get_next_bit(self):
        if self.idx >= len(self.bits):
            raise ValueError("You're out of bits mofo!")
        result = self.bits[self.idx]
        self.idx += 1
        return result

    def get_int(self, bit_count: int) -> int:
        """
        Read the next bit_count bits and return the int value
        """
        result = 0
        s = ""
        for _ in range(bit_count):
            this_bit = self.get_next_bit()
            result *= 2
            result += this_bit
            s += str(this_bit)
        print(f"Returning {bit_count} bits ({s}) -> {result}")
        return result

    def bits_remaining(self):
        return len(self.bits) - self.idx

    def get_bits(self, bit_count: int) -> int:
        """
        Get a big selection of bits as a list
        """
        result = list(self.bits[self.idx : self.idx + bit_count])
        self.idx += bit_count
        return result


# Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
# Packets with type ID 1 are product packets - their value is the result of multiplying together the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
# Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
# Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
# Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is greater than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
# Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
# Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal to the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.


class Packet:
    TYPE_UNKNOWN = -1
    TYPE_SUM = 0
    TYPE_PRODUCT = 1
    TYPE_MIN = 2
    TYPE_MAX = 3
    TYPE_GT = 5
    TYPE_LT = 6
    TYPE_EQUAL = 7
    TYPE_LITERAL = 4

    def __init__(self, bits, depth=0) -> None:
        self.version = -1
        self.type = Packet.TYPE_UNKNOWN
        self.value = None
        self.depth = depth
        self.child_packets = []
        # and parse the real bits..
        self.parse(bits)

    def __repr__(self) -> str:
        padding = "--" * self.depth
        result = f"{padding}Packet<ver={self.version}, type={self.type}, value={self.value}>\n"
        for this_packet in self.child_packets:
            result += str(this_packet)

        return result

    def evaluate(self):
        """
        Return the value for this packet
        """
        child_values = [p.evaluate() for p in self.child_packets]

        if self.type == Packet.TYPE_SUM:
            result = sum(child_values)
        elif self.type == Packet.TYPE_PRODUCT:
            result = 1
            for x in child_values:
                result *= x
        elif self.type == Packet.TYPE_MIN:
            result = min(child_values)
        elif self.type == Packet.TYPE_MAX:
            result = max(child_values)
        elif self.type == Packet.TYPE_GT:
            if child_values[0] > child_values[1]:
                result = 1
            else:
                result = 0
        elif self.type == Packet.TYPE_LT:
            if child_values[0] < child_values[1]:
                result = 1
            else:
                result = 0
        elif self.type == Packet.TYPE_EQUAL:
            if child_values[0] == child_values[1]:
                result = 1
            else:
                result = 0
        elif self.type == Packet.TYPE_LITERAL:
            return self.value
        else:
            raise ValueError(f"What the hell is a {self.type} operator ???")
        return result

    def sum_versions(self):
        """
        Return the sum of the version of this packet and all child-packets
        """
        result = self.version
        for this_child in self.child_packets:
            result += this_child.sum_versions()
        return result

    def parse(self, bits):
        """
        Parse this single packet from bits
        """
        self.version = bits.get_int(3)
        self.type = bits.get_int(3)
        # ok, is this a value packet ?
        if Packet.TYPE_LITERAL == self.type:
            print(f"Parsing a literal packet..{bits.bits_remaining()} bits remaining")
            the_value = 0
            continuation = bits.get_next_bit()
            print(f"Initial continuation bit is {continuation}")
            bits_consumed = 7  # version, type and initial flag bit
            while continuation:
                the_value *= 16
                the_value += bits.get_int(4)
                continuation = bits.get_next_bit()
                bits_consumed += 5
            the_value *= 16
            the_value += bits.get_int(4)
            bits_consumed += 4
            # we're done - got the number..
            self.value = the_value

            # I have misunderstood this bit - it's never necessary ?
            if False:
                # ok, we need the bits consumed to be a multiple of 4
                odd_bits = bits_consumed % 4
                if 0 != odd_bits:
                    padding_bits = 4 - odd_bits
                    # only consume if available - this is sketchy..
                    padding_bits = min(padding_bits, bits.bits_remaining())
                    print(f"Need to consume {padding_bits} padding bits")
                    _ = bits.get_int(padding_bits)

        else:
            # nested packet:
            #     If the length type ID is 0, then the next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet.
            #     If the length type ID is 1, then the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet.
            print(f"Parsing an operator packet (depth={self.depth})")
            length_type = bits.get_next_bit()
            if length_type:
                number_of_sub_packets = bits.get_int(11)
                for this_packet_number in range(number_of_sub_packets):
                    print(
                        f"Parsing an operator packet with {number_of_sub_packets} sub packets. Packet number {this_packet_number}"
                    )
                    this_child_packet = Packet(bits, self.depth + 1)
                    self.child_packets.append(this_child_packet)
            else:
                packet_length = bits.get_int(15)
                print(f"Packet Length is {packet_length}")
                # get the child bits..
                child_bit_values = bits.get_bits(packet_length)
                child_bits = HexBinaryThingy(child_bit_values)
                while child_bits.bits_remaining():
                    this_child_packet = Packet(child_bits, self.depth + 1)
                    self.child_packets.append(this_child_packet)


def part1(filename: str) -> int:
    """
    Run the part1 logic
    """
    hex_digits = ""
    with open(filename, "r") as f:

        for this_line in f:
            this_line = this_line.strip()
            if "" != this_line:
                hex_digits += this_line

    # load them into the binary provider thingy..
    binary = HexBinaryThingy()
    binary.load_hex_digits(hex_digits)
    print(binary)

    # Create the Packet Parser with these bits..
    container = Packet(binary)
    print(container)

    # return the thingy count thingy TBD
    return container.sum_versions()


def part2(filename: str) -> int:
    """
    Run the part2 logic..
    """
    hex_digits = ""
    with open(filename, "r") as f:

        for this_line in f:
            this_line = this_line.strip()
            if "" != this_line:
                hex_digits += this_line

    # load them into the binary provider thingy..
    binary = HexBinaryThingy()
    binary.load_hex_digits(hex_digits)

    # Create the Packet Parser with these bits..
    container = Packet(binary)
    result = container.evaluate()

    # return the thingy count thingy TBD
    return result


def bin_to_hex(bits: str):
    """
    Return a hex string for a binary string
    """
    hexit_for_bits = {
        "0000": "0",
        "0001": "1",
        "0010": "2",
        "0011": "3",
        "0100": "4",
        "0101": "5",
        "0110": "6",
        "0111": "7",
        "1000": "8",
        "1001": "9",
        "1010": "A",
        "1011": "B",
        "1100": "C",
        "1101": "D",
        "1110": "E",
        "1111": "F",
    }
    result = ""
    while "" != bits:
        chunk = bits[:4]
        bits = bits[4:]
        result += hexit_for_bits[chunk]
    return result


def sanity_check():
    """
    Logical check for some of the logic..
    """

    # 110100101111111000101000 -> Logical value 2021
    hex = bin_to_hex("110100101111111000101000")
    binary = HexBinaryThingy()
    binary.load_hex_digits(hex)
    container = Packet(binary)
    print(container)

    # Part 2 sanity check..

    # C200B40A82 finds the sum of 1 and 2, resulting in the value 3.
    # 04005AC33890 finds the product of 6 and 9, resulting in the value 54.
    # 880086C3E88112 finds the minimum of 7, 8, and 9, resulting in the value 7.
    # CE00C43D881120 finds the maximum of 7, 8, and 9, resulting in the value 9.
    # D8005AC2A8F0 produces 1, because 5 is less than 15.
    # F600BC2D8F produces 0, because 5 is not greater than 15.
    # 9C005AC2F8F0 produces 0, because 5 is not equal to 15.
    # 9C0141080250320F1802104A08 produces 1, because 1 + 3 = 2 * 2.

    evaluation_tests = [
        ("C200B40A82", 3),
        ("04005AC33890", 54),
        ("880086C3E88112", 7),
        ("CE00C43D881120", 9),
        ("D8005AC2A8F0", 1),
        ("F600BC2D8F", 0),
        ("9C005AC2F8F0", 0),
        ("9C0141080250320F1802104A08", 1),
    ]
    for hex, expected in evaluation_tests:
        binary = HexBinaryThingy()
        binary.load_hex_digits(hex)
        container = Packet(binary)
        actual = container.evaluate()
        print(f"Input {hex}, got {actual}, expected {expected}")
        assert actual == expected


if __name__ == "__main__":
    sanity_check()

    test_info = [
        ("test1_input.txt", 16),
        ("test2_input.txt", 12),
        ("test3_input.txt", 23),
        ("test4_input.txt", 31),
    ]

    for test_filename, test_expected in test_info:
        actual = part1(test_filename)
        print(f"Ran file {test_filename}, got {actual}, expected {test_expected}")
        assert actual == test_expected

    puzzle_filename = "puzzle_input.txt"
    puzz1 = part1(puzzle_filename)
    print(f"Part 1 actual result : {puzz1}")

    puzz2 = part2(puzzle_filename)
    print(f"Part 2 actual result : {puzz2}")
