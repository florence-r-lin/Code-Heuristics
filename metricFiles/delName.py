import os

def delName(folderPath):
    textExtensions = ['.txt', '.py', '.ipynb', '.html', '.csv', '.md']

    for root, dirs, files in os.walk(folderPath):
        for file in files:
            filePath = os.path.join(root, file)

            if not any(file.lower().endswith(ext) for ext in textExtensions):
                continue

            try:
                folderName = os.path.basename(root)
                name = folderName.rsplit(' ', 1)[0] if folderName.endswith(' NI') else folderName

                # remove 'AM' from file name
                initials = ''.join([part[0] for part in name.split() if part])
                unwanted = [initials]
                for part in unwanted:
                    if part in file:
                        newFileName = file.replace(part, '')
                        newFilePath = os.path.join(root, newFileName)
                        os.rename(filePath, newFilePath)
                        print(f'Renamed {file} as {newFileName}')
                        filePath = newFilePath
                        file = newFileName

                with open(filePath, 'r') as f:
                            fileContent = f.readlines()

                # remove 'Alexis Mumbo' from file
                newContent = [line.replace(name, '') for line in fileContent]

                if newContent != fileContent:
                    print(f'Deleted {name} in {filePath}')
                    with open(filePath, 'w') as f:
                         f.writelines(newContent)

            except Exception as e:
                 print(f'{e} in {filePath}')

    """
    subdirs = [d for d in os.listdir(folderPath) if os.path.isdir(os.path.join(folderPath, d))]
    subdirs.sort()
    for idx, oldFolderName in enumerate(subdirs, start=1):
        newFolderName = f"submission_176{idx}"
        oldFolderPath = os.path.join(folderPath, oldFolderName)
        newFolderPath = os.path.join(folderPath, newFolderName)

        try:
            os.rename(oldFolderPath, newFolderPath)
            print(f'Renamed {oldFolderName} as {newFolderName}')
        except Exception as e:
            print(f'{e} in {oldFolderPath}')
    """

# folderPath = '/Users/summer-2024/Desktop/code metrics 25/All-Data/CS35-Data/assignments postllm/submissions_cs35_sp2025/'
folderPath = '/Users/summer-2024/Desktop/code metrics 25/All-Data/ECON176-Data/assignments postllm/submissions_econ176_sp2025/'
# folderPath = '/Users/summer-2024/Desktop/code metrics 25/All-Data/IST341-Data/assignments postllm/submissions_ist341_sp2025/'

delName(folderPath)