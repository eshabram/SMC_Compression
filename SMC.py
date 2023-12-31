import argparse
import pdb
from seq2seq_unigram import *
from huffman import *
from utils import *
import os
import threading


def compress(args):
    file_name = get_filename_without_extension(args.filepath)
    
    """Pdf """
    if args.filepath[-3:] == 'pdf':
        file_content = extract_text_from_pdf(args.filepath)
        encoded_data = binary_encode(file_content, args)
    else:
        with open(args.filepath, 'r') as file:
            file_content = file.read()
            encoded_data = binary_encode(file_content, args)

    # Apped '.smc' extension
    file_directory, file_name_with_extension = os.path.split(args.filepath)
    file_name, file_extension = os.path.splitext(file_name_with_extension)
    new_file_path = os.path.join(file_directory, f"{file_name}{file_extension}.smc")

    
    # Write the encoded data to the new file
    with open(new_file_path, 'wb') as new_file:
        new_file.write(encoded_data)
        
def decompress(args):
    if args.filepath[-3:] != 'smc' and not args.force:
        print(args.filepath[-3:])
        print(args.filepath[-7:-4])
        print('Incorrect filetype. Please use .smc filetype.')
        exit()
        
    # read binary file
    with open(args.filepath, 'rb') as file:
        file_data = file.read()
        file_content = ''.join(format(byte, '08b') for byte in file_data)
        decoded_data = decode_sequence(file_content, args)
        if args.filepath[-7:-4] == 'pdf':
            decoded_data = create_pdf_from_text(decoded_data)

        
        # Trim the '.smc' extension
        file_directory, file_name_with_extension = os.path.split(args.filepath)
        file_name, file_extension = os.path.splitext(file_name_with_extension)
        new_file_path = os.path.join(file_directory, f"{file_name}.uncompressed")


        # Write the encoded data to the new file
        with open(new_file_path, 'w') as new_file:
            new_file.write(decoded_data)


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("filepath", type=str, help="File path to be compressed.")
    parser.add_argument("-v", "--verbose", \
                        action="store_true", help="Enable verbose mode.")
    parser.add_argument("--huffman", \
                        action="store_true", help="Measure message against Huffman coding.")
    parser.add_argument("-d", "--decompress", \
                        action="store_true", help="Decompress SMC file.")
    parser.add_argument("-f", "--force", \
                        action="store_true", help="Enable test mode.")
    parser.add_argument("-t", "--test", \
                        action="store_true", help="Enable test mode.")
    parser.add_argument("-p", "--pdf", \
                        action="store_true", help="Read in pdf as input")
    args = parser.parse_args()
    if args.pdf:
        file_content = extract_text_from_pdf(args.filepath)
        with open('temp.txt', 'w') as file:
            file.write(file_content)
    # threadlocker = threading.Lock()
    # animation_event = threading.Event()
    # animation_thread = threading.Thread(target=loading_animation)
    if args.test and args.filepath:
        process_file(args.test, 'temp.txt')
        exit()
    # animation_thread.start()
    if args.decompress:
        decompress(args)
    else:
        compress(args)
    # animation_event.set()
    # animation_thread.join()
    
    