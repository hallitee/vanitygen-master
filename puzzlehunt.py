import subprocess
import time
import os
from decimal import Decimal
import base58
import hashlib
import ecdsa

# Function to clear the terminal screen
def clear_terminal():
    subprocess.call('clear', shell=True)

# Function to convert a decimal number to a compressed Bitcoin address
def decimal_to_compressed_address(decimal_number):
    private_key = int(decimal_number).to_bytes(32, byteorder='big')
    signing_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
    verifying_key = signing_key.verifying_key
    compressed_public_key = verifying_key.to_string("compressed")
    hashed_string = hashlib.sha256(compressed_public_key).digest()
    ripemd_string = hashlib.new('ripemd160', hashed_string).digest()
    ripemd_string = b'\x00' + ripemd_string
    hashed_string = hashlib.sha256(ripemd_string).digest()
    hashed_string = hashlib.sha256(hashed_string).digest()
    checksum = hashed_string[:4]
    address = ripemd_string + checksum
    base58_address = base58.b58encode(address)
    return base58_address.decode()

# Function to convert a decimal number to a private key in hexadecimal format
def decimal_to_private_key_hex(decimal_number):
    private_key_bytes = int(decimal_number).to_bytes(32, byteorder='big')
    private_key_hex = private_key_bytes.hex()
    private_key_hex_flipped = private_key_hex.replace('2', '3', 2)
    return private_key_hex, private_key_hex_flipped

# Function to check if a target address is found
def check_target_address(address, decimal_number, private_key_hex):
    if address in target_addresses:
        target_addresses_found.append(address)
        print(f"Target address found: {address}")
        print(f"Decimal Number: {decimal_number}")
        print(f"Private Key Hex: {private_key_hex}")

        # Write the found address to the file add to found addresses.txt
        with open("found_addresses.txt", "a") as found_file:
            found_file.write(f"Target address found: {address}\n")
            found_file.write(f"Decimal Number: {decimal_number}\n")
            found_file.write(f"Private Key Hex: {private_key_hex}\n\n")
            found_file.flush()  # Flush the buffer to ensure data is written immediately

        return True
    return False

# List of target Bitcoin addresses to search for
target_addresses = ['13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so', '1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9', '1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ', '19vkiEajfhuZ8bs8Zu2jgmC6oqZbWqhxhG', '1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU']

# List of additional hex numbers to modify the decimal number
additional_hex_numbers = ['3','4','5','6','7','8', '9', 'a', 'b', 'c', 'd', 'e', 'f','10','11','12','13','14','15','16','17','18','19','1a', '1b', '1c','1d', '1e', '1f'
,'40','41','42','43','44','45','46','47','48','49','4a', '4b', '4c','4d', '4e', '4f' ,'50','51','52','53','54','55','56','57','58','59','5a', '5b', '5c','5d', '5e', '5f' ,'60','61','62','63','64','65','66','67','68','69','6a', '6b', '6c','6d', '6e', '6f' ,'70','71','72','73','74','75','76','77','78','79','7a', '7b', '7c','7d', '7e', '7f' ]

# Define the lower and upper bounds for the decimal number search range
lower_bound = Decimal('37000000000000000000')
upper_bound = Decimal('55340232221128654832')

target_addresses_found = []

# Initialize time and iteration tracking variables
start_time = time.time()
total_iterations = 0

# Function to search for target addresses within a specified range
def search_decimal_range(decimal_number, upper_bound):
    global total_iterations  # Use the global variable
    iterations = 0
    update_interval = 1
    step_size = 100000000000000  # Initial step size

    while decimal_number <= upper_bound:
        compressed_address = decimal_to_compressed_address(decimal_number)
        private_key_hex, flipped_private_key_hex = decimal_to_private_key_hex(decimal_number)

        if check_target_address(compressed_address, decimal_number, private_key_hex):
            return True  # Stop the loop if a match is found

        found_match = False

        additional_addresses = []
        for hex_number in additional_hex_numbers:
            modified_decimal_number = int(hex(int(decimal_number))[2:].replace('2', hex_number, 1), 16)
            modified_compressed_address = decimal_to_compressed_address(modified_decimal_number)
            additional_addresses.append(modified_compressed_address)

            if check_target_address(modified_compressed_address, modified_decimal_number, private_key_hex):
                found_match = True
                break

        if found_match:
            return True

        if len(target_addresses_found) == len(target_addresses):
            return True

        if iterations % update_interval == 0:
            elapsed_time = time.time() - start_time
            iterations_per_second = iterations / elapsed_time
            print(f"Reached {iterations} iterations.")
            print(f"Elapsed Time: {elapsed_time:.2f} seconds")
            print(f"Iterations per Second: {iterations_per_second:.2f}")
            print(f"Decimal Number: {decimal_number}")
            print(f"Compressed Bitcoin Address: {compressed_address}")
            print(f"Private Key Hex: {private_key_hex}")
            if target_addresses_found:
                print_addresses_side_by_side(target_addresses_found[-1], decimal_number, private_key_hex, additional_addresses)
            print("\n")

        if iterations % 100000 == 0:
            clear_terminal()

        decimal_number += step_size  # Increase the decimal number by the current step size
        iterations += 1

        # Adjust the step size dynamically based on the search space
        if iterations % 1000 == 0:
            step_size *= 2  # Double the step size every 1 million iterations

# Function to print the target address and additional addresses side by side
def print_addresses_side_by_side(target_address, decimal_number, private_key_hex, additional_addresses):
    print(f"Decimal Number: {decimal_number}")
    print(f"Target Address: {target_address}")
    print(f"Private Key Hex: {private_key_hex}")
    for i, address in enumerate(additional_addresses):
        print(f" ({additional_hex_numbers[i]}): {address}")
    print("\n")

# Function to continuously search for target addresses in the specified range
def continuous_search(lower_bound, upper_bound):
    global total_iterations, start_time  # Use the global variables
    current_decimal = lower_bound

    while True:
        elapsed_time = time.time() - start_time
        total_iterations += 1

        if search_decimal_range(current_decimal, upper_bound):
            print("All target addresses found. Restarting search...")
            time.sleep(0)  # Optional: Add a delay before restarting the search
            current_decimal = lower_bound  # Reset the current_decimal to the lower_bound
        else:
            current_decimal += 1  # Increment by 1

# Start the continuous search
while True:
    continuous_search(lower_bound, upper_bound)

# Add sound notification when the script completes
# print("Glass sound (indicating script completion)")
# # subprocess.run(["afplay", "/System/Library/Sounds/glass.aiff"])