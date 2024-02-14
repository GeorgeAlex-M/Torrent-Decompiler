import bencode
import json
import os
import sys
from pathlib import Path

def get_path_relative_to_script(filename):
    if getattr(sys, 'frozen', False):
        script_dir = Path(os.path.dirname(sys.executable))
    else:
        script_dir = Path(__file__).parent

    return script_dir / filename

def convert_bytes_to_str(data):
    if isinstance(data, bytes):
        # Special handling for the 'pieces' field in torrent files
        if len(data) == 20:  # Length of a SHA-1 hash value
            return data.hex()  # Convert bytes to hexadecimal
        return data.decode('utf-8', 'ignore')
    elif isinstance(data, dict):
        return {k: convert_bytes_to_str(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_bytes_to_str(element) for element in data]
    else:
        return data

def decode_and_save_torrent_file(torrent_filename, output_filename):
    try:
        with open(get_path_relative_to_script(torrent_filename), 'rb') as file:
            torrent_data = file.read()
            decoded_data = bencode.bdecode(torrent_data)

        converted_data = convert_bytes_to_str(decoded_data)

        with open(get_path_relative_to_script(output_filename), 'w') as file:
            json.dump(converted_data, file, indent=4, sort_keys=True)

        print(f"Decompiled data saved to {output_filename}")
    except FileNotFoundError:
        print(f"The file {torrent_filename} was not found.")
    except bencode.BencodeDecodeError as e:
        print(f"Error decoding the file: {e}")

if __name__ == "__main__":
    torrent_filename = 'name.torrent'  # .torrent file name
    output_filename = 'decompiled_output.json'  # Output file name
    decode_and_save_torrent_file(torrent_filename, output_filename)
