# utils.py

def compute_parity_bits(pid_bits):
    p0 = pid_bits[0] ^ pid_bits[1] ^ pid_bits[2] ^ pid_bits[4]
    p1 = ~(pid_bits[1] ^ pid_bits[3] ^ pid_bits[4] ^ pid_bits[5]) & 0x1
    return p0, p1


def compute_checksum(data_bytes):
    data = 0
    for i, b in enumerate(data_bytes):
        for j in range(8):
            bit = (b >> j) & 1
            data |= bit << (8 * i + j)

    crc_in = 0xFF
    d = [(data >> i) & 1 for i in range(64)]
    c = [(crc_in >> i) & 1 for i in range(8)]

    crc_out = [0] * 8
    crc_out[0] = c[0] ^ c[4] ^ c[7] ^ d[0] ^ d[6] ^ d[7] ^ d[8] ^ d[12] ^ d[14] ^ d[16] ^ d[18] ^ d[19] ^ d[21] ^ d[23] ^ d[28] ^ d[30] ^ d[31] ^ d[34] ^ d[35] ^ d[39] ^ d[40] ^ d[43] ^ d[45] ^ d[48] ^ d[49] ^ d[50] ^ d[52] ^ d[53] ^ d[54] ^ d[56] ^ d[60] ^ d[63]
    crc_out[1] = c[0] ^ c[1] ^ c[4] ^ c[5] ^ c[7] ^ d[0] ^ d[1] ^ d[6] ^ d[9] ^ d[12] ^ d[13] ^ d[14] ^ d[15] ^ d[16] ^ d[17] ^ d[18] ^ d[20] ^ d[21] ^ d[22] ^ d[23] ^ d[24] ^ d[28] ^ d[29] ^ d[30] ^ d[32] ^ d[34] ^ d[36] ^ d[39] ^ d[41] ^ d[43] ^ d[44] ^ d[45] ^ d[46] ^ d[48] ^ d[51] ^ d[52] ^ d[55] ^ d[56] ^ d[57] ^ d[60] ^ d[61] ^ d[63]
    crc_out[2] = c[1] ^ c[2] ^ c[4] ^ c[5] ^ c[6] ^ c[7] ^ d[0] ^ d[1] ^ d[2] ^ d[6] ^ d[8] ^ d[10] ^ d[12] ^ d[13] ^ d[15] ^ d[17] ^ d[22] ^ d[24] ^ d[25] ^ d[28] ^ d[29] ^ d[33] ^ d[34] ^ d[37] ^ d[39] ^ d[42] ^ d[43] ^ d[44] ^ d[46] ^ d[47] ^ d[48] ^ d[50] ^ d[54] ^ d[57] ^ d[58] ^ d[60] ^ d[61] ^ d[62] ^ d[63]
    crc_out[3] = c[2] ^ c[3] ^ c[5] ^ c[6] ^ c[7] ^ d[1] ^ d[2] ^ d[3] ^ d[7] ^ d[9] ^ d[11] ^ d[13] ^ d[14] ^ d[16] ^ d[18] ^ d[23] ^ d[25] ^ d[26] ^ d[29] ^ d[30] ^ d[34] ^ d[35] ^ d[38] ^ d[40] ^ d[43] ^ d[44] ^ d[45] ^ d[47] ^ d[48] ^ d[49] ^ d[51] ^ d[55] ^ d[58] ^ d[59] ^ d[61] ^ d[62] ^ d[63]
    crc_out[4] = c[0] ^ c[3] ^ c[4] ^ c[6] ^ c[7] ^ d[2] ^ d[3] ^ d[4] ^ d[8] ^ d[10] ^ d[12] ^ d[14] ^ d[15] ^ d[17] ^ d[19] ^ d[24] ^ d[26] ^ d[27] ^ d[30] ^ d[31] ^ d[35] ^ d[36] ^ d[39] ^ d[41] ^ d[44] ^ d[45] ^ d[46] ^ d[48] ^ d[49] ^ d[50] ^ d[52] ^ d[56] ^ d[59] ^ d[60] ^ d[62] ^ d[63]
    crc_out[5] = c[1] ^ c[4] ^ c[5] ^ c[7] ^ d[3] ^ d[4] ^ d[5] ^ d[9] ^ d[11] ^ d[13] ^ d[15] ^ d[16] ^ d[18] ^ d[20] ^ d[25] ^ d[27] ^ d[28] ^ d[31] ^ d[32] ^ d[36] ^ d[37] ^ d[40] ^ d[42] ^ d[45] ^ d[46] ^ d[47] ^ d[49] ^ d[50] ^ d[51] ^ d[53] ^ d[57] ^ d[60] ^ d[61] ^ d[63]
    crc_out[6] = c[2] ^ c[5] ^ c[6] ^ d[4] ^ d[5] ^ d[6] ^ d[10] ^ d[12] ^ d[14] ^ d[16] ^ d[17] ^ d[19] ^ d[21] ^ d[26] ^ d[28] ^ d[29] ^ d[32] ^ d[33] ^ d[37] ^ d[38] ^ d[41] ^ d[43] ^ d[46] ^ d[47] ^ d[48] ^ d[50] ^ d[51] ^ d[52] ^ d[54] ^ d[58] ^ d[61] ^ d[62]
    crc_out[7] = c[3] ^ c[6] ^ c[7] ^ d[5] ^ d[6] ^ d[7] ^ d[11] ^ d[13] ^ d[15] ^ d[17] ^ d[18] ^ d[20] ^ d[22] ^ d[27] ^ d[29] ^ d[30] ^ d[33] ^ d[34] ^ d[38] ^ d[39] ^ d[42] ^ d[44] ^ d[47] ^ d[48] ^ d[49] ^ d[51] ^ d[52] ^ d[53] ^ d[55] ^ d[59] ^ d[62] ^ d[63]

    # Pack result (LSB-first)
    
    return sum((crc_out[i] & 1) << i for i in range(8))


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
        bits = [0] + [int(x) for x in f"{byte:08b}"[::-1]] + [1]
        response_bits.extend(bits)

    checksum = compute_checksum(data_bytes)
    checksum_bits = [0] + [int(x) for x in f"{checksum:08b}"[::-1]] + [1]
    response_bits.extend(checksum_bits)

    response_value = 0
    for bit in response_bits:
        response_value = (response_value << 1) | bit
    return response_value, response_bits
