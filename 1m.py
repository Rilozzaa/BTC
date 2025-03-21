from bitcoin import privtopub, pubkey_to_address, encode_privkey
import os
import random
import secrets

start = 0x000000000000000000000000000000000000000000000080000000000000000
end = 0x0000000000000000000000000000000000000000000000fffffffffffffffff
target_address = "1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ"

status_file = "last_scanned_key.txt"

def load_last_scanned():
    if os.path.exists(status_file):
        with open(status_file, "r") as f:
            return int(f.read().strip(), 16)
    return None

def save_last_scanned(privkey_int):
    with open(status_file, "w") as f:
        f.write(hex(privkey_int))

def compress_pubkey(pubkey_hex):
    if pubkey_hex[0:2] != "04":
        raise ValueError("Invalid uncompressed public key")
    x = pubkey_hex[2:66]
    y = int(pubkey_hex[66:], 16)
    prefix = "02" if y % 2 == 0 else "03"
    return prefix + x

def random_private_key(start, end):
    return secrets.randbelow(end - start + 1) + start

last_scanned_key = load_last_scanned()

if last_scanned_key:
    print(f"Resuming from last scanned key: {hex(last_scanned_key)}")
else:
    print("Starting fresh...")

while True:

    current_key = random_private_key(start, end)
    
    privkey_hex = encode_privkey(current_key, 'hex')
    pubkey_uncompressed = privtopub(privkey_hex)
    pubkey_compressed = compress_pubkey(pubkey_uncompressed)
    address_uncompressed = pubkey_to_address(pubkey_uncompressed)
    address_compressed = pubkey_to_address(pubkey_compressed)

    print(f"Hex: {hex(current_key)}")
    print(f"Private Key (Hexadecimal): {privkey_hex}")
    print(f"Uncompressed Address: {address_uncompressed}")
    print(f"Compressed Address: {address_compressed}\n")

    save_last_scanned(current_key)

    if address_uncompressed == target_address or address_compressed == target_address:
        print("Target address found!")
        break
