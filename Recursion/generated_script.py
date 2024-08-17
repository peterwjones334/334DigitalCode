import sys

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
        print(contents)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generated_script.py <file_to_read>")
    else:
        file_path = sys.argv[1]
        read_file(file_path)

# Automatically generated script to read and print file contents
# File to read: example.txt
