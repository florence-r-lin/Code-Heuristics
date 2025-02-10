import os
cwd = str(os.getcwd()) + "/jupyterToPy" #This is meant to be the exact file path that holds the ipynb files

#If there is not a folder called pyToText to place final documents, make one
if not os.path.isdir(str(os.getcwd()) + "/pyToText"):
    os.mkdir("pyToText")

#Take all python files and convert them to text files using the rename functionality
for file in os.listdir(cwd):
    if file[-1] == "y":
        os.rename(cwd + "/" + file, cwd + "/" + file[:-3] + ".txt")

#Take all text files, seperate markdown and python into seperate files
for file in os.listdir(cwd):
    if file[-1] == "t":
        print(file)
        with open(cwd + "/" + file, 'r') as tFile:
            newT = open(str(os.getcwd()) + "/pyToText/" + file[:-4] + "-code.txt", 'w')
            markT = open(str(os.getcwd()) + "/pyToText/" + file[:-4] + "-mark.txt", 'w')
            codeBlock = False
            for line in tFile:
                if "# -" == line[:3] or "# +" == line[:3]: #code line has ended or begun
                    if "# -" == line[:3]:
                        codeBlock = False
                    else:
                        codeBlock = True
                else: # If not a stop or start line write to corresponding text doc or markdown doc
                    if codeBlock:
                        newT.write(line) 
                    else:
                        markT.write(line)
            newT.close()




                    