import os
import rarfile
import shutil

def rename_files_in_numerical_order(directory):
    # List all files in the directory
    files = sorted(os.listdir(directory))
    
    # Rename files in numerical order
    for index, file in enumerate(files, start=1):
        old_path = os.path.join(directory, file)
        new_filename = f"{index:03d}{os.path.splitext(file)[1]}"
        new_path = os.path.join(directory, new_filename)
        os.rename(old_path, new_path)
        print(f"Renamed '{file}' to '{new_filename}'")

def create_cbr_file(directory, output_filename):
    # Create a temporary RAR file
    temp_rar_path = f"{output_filename}.rar"
    with rarfile.RarFile(temp_rar_path, 'w') as rf:
        # Add files to RAR archive
        for file in sorted(os.listdir(directory)):
            file_path = os.path.join(directory, file)
            rf.write(file_path, arcname=file)
            print(f"Added '{file}' to RAR archive")
    
    # Rename RAR file to CBR
    cbr_path = f"{output_filename}.cbr"
    shutil.move(temp_rar_path, cbr_path)
    print(f"Created CBR file: {cbr_path}")

# Specify the directory of your files
directory = 'C:\\WorkArea\\ProjectX\\Image'

# Specify the desired output filename for the CBR file (without extension)
output_filename = 'MyCBR'

# Rename files in numerical order
rename_files_in_numerical_order(directory)

# Create a CBR file from the renamed files
create_cbr_file(directory, output_filename)
