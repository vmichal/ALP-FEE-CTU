import sys

parity_to_data = [(1, (3,5,7,9,11)),
    (2, (3,6,7,10,11)),
    (4, (5,6,7,12)),
    (8, (9,10,11,12))]


def error():
    print('ERROR')
    sys.exit()

def encode(char):

    character_bits = list(map(lambda digit: 1 if digit == '1' else 0, reversed('0' * 8 + bin(ord(char))[2:])))
    code = [None] + [0] * 12
    code[3] = character_bits[0]
    code[5], code[6], code[7] = character_bits[1], character_bits[2], character_bits[3]
    code[9], code[10], code[11], code[12] = character_bits[4], character_bits[5], character_bits[6], character_bits[7]
    for parity, data in parity_to_data:
        code[parity] = sum((code[i] for i in data))
        code[parity] %= 2

    return code[1:]


def validate(line):
    line = line.strip()
    if len(line) != 12 or not set(line) <= set(('1', '0')):
        error()
    return [None] + list(map(lambda x: int(x, 2), line))


def raw_value(code):
    return code[3] | code[5] << 1 | code[6] << 2 | code[7] << 3 | code[9] << 4 | code[10] << 5 | code[11] << 6 | code[12] << 7


def decode(lines):
    output = []
    for code in map(validate, lines):
        value = raw_value(code)
        ideal = [None] + encode(chr(value))

        error_bits = set(list(range(1,13))).difference(set([1,2,4,8]))

        for parity, dependent_bits in parity_to_data:
            operation = set.difference if code[parity] == ideal[parity] else set.intersection
            error_bits = operation(error_bits, dependent_bits)

        error_bits = list(error_bits)
        if len(error_bits) == 1:
            code[error_bits[0]] ^= 1

        output.append((chr(raw_value(code))))
    return output
                                                                

if __name__ == '__main__':
    line = input()
    if line[0] == 'c':
        for char in line[1:]:
            print(''.join(list(map(lambda bit: '1' if bit else '0', encode(char)))))
    elif line[0] == 'd':
        print(''.join(decode(sys.stdin.readlines())))
    else:
        error()
