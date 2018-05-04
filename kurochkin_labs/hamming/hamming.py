import os
import numpy as np
import binascii

segment_size = 54


global_encoded_text = ''
global_read_text = ''
global_res = ''
def encode_segment(segment):
    control_bit_cnt = 0
    while (1 << control_bit_cnt) < len(segment) + control_bit_cnt
        control_bit_cnt += 1
    print(control_bit_cnt)
    segment = np.asarray([int(x) for x in segment])
    matrix = np.zeros((len(segment), control_bit_cnt), dtype=np.int32)
    for i in range(1, len(segment) + 1):
        for j in range(control_bit_cnt):
            b = int(  (i & (1 << j)  ) > 0 )
            matrix[i - 1][j] = b

    res = segment.dot(matrix)
    for i in range(len(res)):
        res[i] = res[i] & 1
    print('control_bits', res)
    for i in range(control_bit_cnt):
        if i == 0:
            segment[i] = res[i]
        else:
            segment[(1 << i) - 1] = res[i]
    return segment

def encode_text(segments):
    text = ''
    for seg in segments:
        en = encode_segment(seg)
        for x in en:
            text += str(x)
    return text


def encode_file(input_filename, output_filename):
    with open(input_filepath, 'r', encoding='utf8') as file:
        input_data = file.read()

    res = bin(int.from_bytes(input_data.encode(), 'big'))
    global_res = res
    # n = int(res, 2)
    # print( n.to_bytes((n.bit_length() + 7) // 8, 'big').decode() )
    # print(res)
    res = res[2:]
    print(len(res))
    len_res = len(res)
    segments = [res[i * segment_size: min(len_res, (i + 1) * segment_size)] for i in range(int(len_res / segment_size) + 1)]

    while len(segments[-1]) < segment_size:
        segments[-1] += '0'

    for x in segments:
        print(x, len(x))

    new_segments = list()
    for seg in segments:
        shift = 0
        cur_seg = seg
        while True:
            if shift == 0:
                p2 = 0
            else:
                p2 = (1 << shift) - 1
            if p2 > len(cur_seg):
                new_segments.append(cur_seg)
                break
            shift += 1
            cur_seg = cur_seg[:p2] + '0' + cur_seg[p2:]
    for x in new_segments:
        print(x, len(x))

    en_text = encode_text(new_segments)
    from copy import copy
    with open(output_filename, 'w', encoding='utf8') as file:
        file.write(en_text)
    return en_text


def decode_segment(segment):
    control_bit_cnt = len(segment) - segment_size
    segment = np.asarray([int(x) for x in segment])
    matrix = np.zeros((len(segment), control_bit_cnt), dtype=np.int32)
    for i in range(1, len(segment) + 1):
        for j in range(control_bit_cnt):
            b = int(  (i & (1 << j)  ) > 0 )
            matrix[i - 1][j] = b

    res = segment.dot(matrix)
    for i in range(len(res)):
        res[i] = res[i] & 1
    print('control_bits', res)
    pos = 0
    for i in range(control_bit_cnt):
        pos |= res[i] << i
    if pos != 0:
        raise("trouble here!!!!")
    p2 = 1
    ans = ''
    for i in range(len(segment)):
        if i == p2 - 1:
            p2 <<= 1
            continue
        else:
            ans += str(segment[i])
    return ans

def decode_text(segments):
    text = '0b'
    for seg in segments:
        text += decode_segment(seg)
    return text

def decode_file(input_filepath, output_filepath, encoded_segment_size):
    with open(input_filepath, 'r', encoding='utf8') as file:
        input_data = file.read()
    len_data = len(input_data)
    encoded_segments = [input_data[i * encoded_segment_size: min(len(input_data), (i + 1) * encoded_segment_size)] for i in range(int(len(input_data) / encoded_segment_size))]
    global_read_text = ''
    print(encoded_segments)
    for s in encoded_segments:
        global_read_text += s
    print('1', global_encoded_text)
    print('2', global_read_text)
    difs = list()
    for i in range(len(global_encoded_text)):
        if global_encoded_text[i] != global_read_text[i]:
            difs.append(i)
    print(difs)
    # exit()
    text = decode_text(encoded_segments)
    with open('input.txt', 'r', encoding='utf8') as file:
        input_data = file.read()

    global_res = bin(int.from_bytes(input_data.encode(), 'big'))
    print('3', text)
    print('4', global_res)
    # exit()
    # cnt = len(text) - (len(encoded_segments) - 1) * segment_size -
    # text = text[:len(text) - cnt]
    text = text[:9]
    n = int(text, 2)
    dec_text = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
    with open(output_filepath, 'w', encoding='utf8') as file:
        file.write(dec_text)


if __name__ == "__main__":
    input_filepath = 'input.txt'
    output_filepath = 'output.txt'
    decoded_filepath = 'decoded.txt'

    global_encoded_text = encode_file(input_filepath, output_filepath)
    decode_file(output_filepath, decoded_filepath, 60)