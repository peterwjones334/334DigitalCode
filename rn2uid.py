import os
import uuid

def rename_files_in_folder(folder_path):
    """Rename all files in the specified folder with UUID names."""
    for filename in os.listdir(folder_path):
        # Check if it's a file and not a folder
        if os.path.isfile(os.path.join(folder_path, filename)):
            # Split the filename into name and extension
            name, ext = os.path.splitext(filename)
            # Generate a new UUID name and add the original extension
            new_name = str(uuid.uuid4()) + ext
            # Construct full file paths
            old_file = os.path.join(folder_path, filename)
            new_file = os.path.join(folder_path, new_name)
            # Rename the file
            os.rename(old_file, new_file)
            print(f'Renamed {filename} to {new_name}')

# Specify the folder path here
folder_path = 'C:\\WorkArea\\ProjectX\\Images'
rename_files_in_folder(folder_path)
