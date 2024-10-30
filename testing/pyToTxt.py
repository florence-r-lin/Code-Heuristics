import os
import shutil


# cd to summer-2024 directory
main_directory = '/Users/summer-2024/Desktop/assignments prellm/'  
all_text_dir = os.path.join(main_directory, 'allText')

for root, dirs, files in os.walk(main_directory):
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(root, file)     
            new_file_path = os.path.join(all_text_dir, f"{os.path.basename(root)}_final.txt")
            shutil.copy(file_path, new_file_path)