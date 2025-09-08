def compute_parity_bits(pid_bits):
    p0 = pid_bits[0] ^ pid_bits[1] ^ pid_bits[2] ^ pid_bits[4]
    p1 = ~(pid_bits[1] ^ pid_bits[3] ^ pid_bits[4] ^ pid_bits[5]) & 0x1
    return p0, p1


def compute_checksum(data_bytes):
    data = 0
    for i, b in enumerate(data_bytes):
        for j in range(8):
            bit = (b >> j) & 1   # LSB-first
            data |= bit << (8 * i + j)

    crc_in = 0xFF
    d = [(data >> i) & 1 for i in range(64)]
    c = [(crc_in >> i) & 1 for i in range(8)]

    crc_out = [0] * 8
    crc_out[0] = c[0] ^ c[4] ^ c[7] ^ d[0] ^ d[6] ^ d[7] ^ d[8] ^ d[12] ^ d[14] ^ d[16] ^ d[18] ^ d[19] ^ d[21] ^ d[23] ^ d[28] ^ d[30] ^ d[31] ^ d[34] ^ d[35] ^ d[39] ^ d[40] ^ d[43] ^ d[45] ^ d[48] ^ d[49] ^ d[52] ^ d[53] ^ d[54] ^ d[56] ^ d[60] ^ d[63]
    # ... keep the rest of your crc_out logic
    checksum = sum((crc_out[i] & 1) << i for i in range(8))
    return checksum


def build_expected_header(pid):
    break_field = [0] * 13
    delimiter = [1]
    sync_bits = [0] + [int(x) for x in f"{0x55:08b}"[::-1]] + [1]

    pid_bits = [(pid >> i) & 1 for i in range(6)]
    p0, p1 = compute_parity_bits(pid_bits)
    pid_full = pid_bits + [p0, p1]
    pid_field = [0] + pid_full + [1]

    header_bits = break_field + delimiter + sync_bits + pid_field

    header_value = 0
    for bit in header_bits:
        header_value = (header_value << 1) | bit

    return header_value, header_bits


def build_expected_response(data_bytes):
    response_bits = []
    for byte in data_bytes:
        bits = [0]
        bits += [int(x) for x in f"{byte:08b}"[::-1]]
        bits += [1]
        response_bits.extend(bits)

    checksum = compute_checksum(data_bytes)
    checksum_bits = [0] + [int(x) for x in f"{checksum:08b}"[::-1]] + [1]
    response_bits.extend(checksum_bits)

    response_value = 0
    for bit in response_bits:
        response_value = (response_value << 1) | bit

    return response_value, response_bits

