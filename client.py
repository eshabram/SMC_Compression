import socket
import argparse
from seq2seq_unigram_freq import binary_encode_simple, binary_encode

def run_client(args):
    print('\n')
    while True:
        try:
            def read_bin(binary_data):
                pad = 0
                binary_data = "".join(str(bit) for bit in binary_string)
                if len(binary_data) % 8 != 0:
                    pad = 8 - len(binary_data)
                if args.verbose:
                    print(f'Binary: {binary_data}')
                    print(f'Binary length = {len(binary_data)} + {pad} padding')
                return len(binary_data) + pad
            
            # get message and encode
            message = input('Enter message: ')
            if len(message) == 0:
                continue
            if args.simple:
                binary_string = binary_encode_simple(message, args)
            else:
                binary_string = binary_encode(message, args)
            if args.verbose:
                print(f'String: {binary_string}')
            
            # Convert binary string to bytes
            while len(binary_string) % 8 != 0:
                binary_string += '0'
                
            binary_data = bytes(int(binary_string[i:i+8], 2) \
                                for i in range(0, len(binary_string), 8))
            
            bin_length = read_bin(binary_data)
            ascii_length = len(message) * 8
            if args.verbose:
                print(f'Message before compression: {ascii_length} bits')
            print(f'Percentage of original size: {bin_length / ascii_length * 100:.3g}%\n')
            
            # Send binary data over the network
            HOST = 'localhost'  # Replace with the server's IP address
            PORT = 12345        # Replace with the desired port number
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(binary_data)
        except KeyboardInterrupt:
            print(' --Program terminated.--')
            break


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-s", "--simple", \
                        action="store_true", help="Enable simple mode.")
    parser.add_argument("-v", "--verbose", \
                        action="store_true", help="Enable verbose mode.")
    args = parser.parse_args()
    run_client(args)