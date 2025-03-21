rom bitcoin import privtopub, pubkey_to_address, encode_privkey
import os

# Rentang private key
start = 0x00000000000000000000000000000000000000000000000b0000000000000000
end = 0x00000000000000000000000000000000000000000000000fffffffffffffffff
target_address = "1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ"

status_file = "last_scanned_key5.txt"
output_file = "found_addresses5.txt"

# Fungsi untuk memuat kunci terakhir yang diperiksa
def load_last_scanned():
    if os.path.exists(status_file):
        with open(status_file, "r") as f:
            content = f.read().strip()
            if content:
                return int(content, 16)
            else:
                print("File kosong, memulai dari kunci awal...")
                return None
    return None

# Fungsi untuk menyimpan kunci terakhir yang diperiksa
def save_last_scanned(privkey_int):
    with open(status_file, "w") as f:
        f.write(hex(privkey_int))

# Fungsi untuk menyimpan alamat yang ditemukan
def save_found_address(privkey_hex, address_uncompressed, address_compressed):
    with open(output_file, "a") as f:
        f.write(f"Private Key: {privkey_hex}\n")
        f.write(f"Uncompressed Address: {address_uncompressed}\n")
        f.write(f"Compressed Address: {address_compressed}\n")
        f.write("-" * 40 + "\n")

# Fungsi untuk mengubah public key ke format terkompresi
def compress_pubkey(pubkey_hex):
    if pubkey_hex[0:2] != "04":
        raise ValueError("Invalid uncompressed public key")
    x = pubkey_hex[2:66]
    y = int(pubkey_hex[66:], 16)
    prefix = "02" if y % 2 == 0 else "03"
    return prefix + x

# Memuat kunci terakhir yang diperiksa
last_scanned_key = load_last_scanned()

if last_scanned_key:
    print(f"Resuming from last scanned key: {hex(last_scanned_key)}")
    current_key = last_scanned_key + 1
else:
    print("Starting fresh...")
    current_key = start

while current_key <= end:
    privkey_hex = encode_privkey(current_key, 'hex')
    pubkey_uncompressed = privtopub(privkey_hex)
    pubkey_compressed = compress_pubkey(pubkey_uncompressed)                                              address_uncompressed = pubkey_to_address(pubkey_uncompressed)
    address_compressed = pubkey_to_address(pubkey_compressed)                                         
    # Simpan kunci terakhir yang diperiksa
    save_last_scanned(current_key)

    # Tampilkan progres
    print(f"Scanning key: {hex(current_key)}")

    # Periksa apakah alamat target ditemukan
    if address_uncompressed == target_address or address_compressed == target_address:
        print(f"Hex: {hex(current_key)}")
        print(f"Private Key (Hexadecimal): {privkey_hex}")
        print(f"Uncompressed Address: {address_uncompressed}")
        print(f"Compressed Address: {address_compressed}")
        print("Target address found!")

        # Simpan ke file jika ditemukan
        save_found_address(privkey_hex, address_uncompressed, address_compressed)
        break

    # Increment key
    current_key += 1

print("Scanning completed.")
