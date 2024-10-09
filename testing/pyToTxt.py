import os
import shutil


# cd to summer-2024 directory
main_directory = '/Users/summer-2024/Desktop/assignment_214232_export'  
all_text_dir = os.path.join(main_directory, 'allText')

if not os.path.exists(all_text_dir):
    os.makedirs(all_text_dir)
    print(f"Created directory: {all_text_dir}")
else:
    print(f"Directory already exists: {all_text_dir}")

for root, dirs, files in os.walk(main_directory):
    for file in files:
        if file == 'final.py':
            print(f"Found final.py in: {root}")
            file_path = os.path.join(root, file)     
            new_file_path = os.path.join(all_text_dir, f"{os.path.basename(root)}_final.txt")
            print(f"Copying {file_path} to {new_file_path}")
            shutil.copy(file_path, new_file_path)
            print(f'Copied {file_path} to {new_file_path}')