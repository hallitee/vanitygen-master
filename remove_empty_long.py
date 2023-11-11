def remove_empty_and_long_lines(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        for line in input_file:
            line = line.rstrip()  # Remove leading/trailing whitespace
            if not line:  # Skip empty lines
                continue
            if len(line) <= 35:  # Keep lines with 35 or fewer characters
                output_file.write(line + '\n')

if __name__ == '__main__':
    input_file_path = 'bit.txt'  # Replace with your input file path
    output_file_path = 'bitclean.txt'  # Replace with your output file path

    remove_empty_and_long_lines(input_file_path, output_file_path)

    print(f"Filtered lines and saved the result to {output_file_path}.")
