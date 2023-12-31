from collections import Counter
import heapq
import argparse
from utils import *
import pdb


def build_huffman_tree(message, reserved_prefix=None): # reserved_prefix is a string (1s and 0s only)
    freq = Counter(message)
    
    if len(freq) == 1:  # Added line
        char = next(iter(freq.keys())) # Added line
        return {char: '0'}  # Added line

    # Add a dummy character with maximum frequency
    if reserved_prefix != None:
        dummy_char = 'DUMMY'
        freq[dummy_char] = float('inf')
    else:
        dummy_char = ''

    heap = [[weight, [char, ""]] for char, weight in freq.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    
    huffman_codes = sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

    # Remove the dummy character
    huffman_codes = [(char, code) for char, code in huffman_codes if char != dummy_char]

    if reserved_prefix:
        for index, (char, code) in enumerate(huffman_codes):
            while code.startswith(reserved_prefix):
                code = '1' + code[1:]
            huffman_codes[index] = (char, code)
    
    return dict(huffman_codes)


def huffman_encode(message, prefix=None):
    huff_dict = build_huffman_tree(message, reserved_prefix=prefix)
    header = ""
    for char, code in huff_dict.items():
        header += format(ord(char), '08b') + format(len(code), '04b') + code

    encoded_message = ''.join([huff_dict[char] for char in message])
    
    return format(len(header), '016b') + header + encoded_message


def huffman_decode(encoded):
    header_length = int(encoded[:16], 2)
    header = encoded[16:16+header_length]
    message = encoded[16+header_length:]

    huff_dict = {}
    while header:
        char = chr(int(header[:8], 2))
        header = header[8:]
        
        code_len = int(header[:4], 2)
        header = header[4:]
        
        code = header[:code_len]
        header = header[code_len:]
        
        huff_dict[code] = char

    decoded = ""
    temp = ""
    for bit in message:
        temp += bit
        if temp in huff_dict:
            decoded += huff_dict[temp]
            temp = ""

    return decoded


def huffman_encode_chunk(message, huff_dict):
    chunk = ""
    for letter in message:
        try:
            chunk += huff_dict[letter]
        except KeyError:
            print('Letter not in dict')
    return chunk


def build_huffman_tree_from_7bit(message, reserved_prefix='0'):
    # Split the message into 7-bit chunks and convert to characters
    chars = [chr(int(message[i:i+7], 2)) for i in range(0, len(message), 7)]

    # Build frequency counter from the characters
    freq = Counter(chars)
    heap = [[weight, [char, ""]] for char, weight in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)

        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]

        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    huffman_codes = sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

    if reserved_prefix:
        for index, (char, code) in enumerate(huffman_codes):
            while code.startswith(reserved_prefix):
                code = '1' + code[1:]
            huffman_codes[index] = (char, code)

    return dict(huffman_codes)


def huffman_encode_7bit(message, prefix=None):
    huffman_tree = build_huffman_tree_from_7bit(message, reserved_prefix=prefix)
    huff_dict = dict(huffman_tree)
    header = ""
    for char, code in huff_dict.items():
        header += format(ord(char), '08b') + format(len(code), '04b') + code

    encoded_message = ''.join([huff_dict[char] for char in message])
    
    return format(len(header), '016b') + header + encoded_message


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This script implements huffman coding.")
    parser.add_argument("-b", "--binary", \
                        action="store_true", help="Enable full printout of message binary.")
    parser.add_argument("-f", "--filepath", action="store", const=None, type=str, nargs="?")
    parser.add_argument("-t", "--test", \
                        action="store_true", help="Enable test mode.")
    args = parser.parse_args()

    # read in a file or take input
    if args.test:
        message = file_to_binary_string(args.filepath)
    else:    
        if args.filepath is not None:
            with open(args.filepath, 'r') as file:
                message = file.read()
        else:
            message = input('Enter message: ')
    
    if args.test:
        encoded = huffman_encode_7bit(message)
    else:
        encoded = huffman_encode(message)
    if len(encoded) > 100 and not args.binary:
        print(f'Encoded: ...{encoded[-100:]}')
    else:
        print(f"Encoded: {encoded}")
    orig_len = len(message) * 8
    encode_len = len(encoded)
    print(f'Original length: {orig_len}')
    print(f'Encoded length: {encode_len}')
    print(f'Percentage compression: {(encode_len / orig_len) * 100:.3g}%')
    # decoded = huffman_decode(encoded)
    # print(f"Decoded: {decoded}")
    
    """
    !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~

    
    """
    
