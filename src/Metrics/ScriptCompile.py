import os

'''
Author: Jenny Ngo
This program combines scripts from a directory and creates both a list and writes it to combined script (combinedScript.py). 

Users may choose to use lists or write to the output file without lists. For clarification, the lists do not occur in the actual combined script.
The lists are only variables of this program.

CHANGE DIRECTORY: line 56
CHANGE OUTPUT FILE: line 57 (set to default combinedScript.py)
CLEAR OUTPUT FILE: line 60

'''
def combineLst(path, listWrite): #takes in an EMPTY list

    if len(listWrite) != 0: #makes sure we write to an empty list
        listWrite = []

    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                filePath = os.path.join(root, file)
                with open(filePath, 'r') as infile:
                    script_content = infile.readlines()
                    listWrite.append({
                        'filePath': filePath,
                        'content': script_content
                    })
    return listWrite

def writeScript(scripts, outputFile):
    with open(outputFile, 'w') as outfile:
        for script in scripts:
            outfile.write(f"# File: {script['filePath']}\n")
            outfile.writelines(script['content'])
            outfile.write("\n\n")

def combineScripts(path, outputFile):
    with open(outputFile, 'w') as outfile:
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith('.py'):
                    filePath = os.path.join(root, file)
                    with open(filePath, 'r') as infile:
                        outfile.write(f"# File: {filePath}\n")
                        outfile.write(infile.read())
                        outfile.write("\n\n")

def clearOutputFile(outputFile):
    with open(outputFile, 'w') as outfile:
        outfile.write("")

# Copy paste this whole block if you want to run it from another file
if __name__ == "__main__":
    path = "studentScripts" # change to directory of folder
    outputFile = "combinedScript.py"
    
    isList = False  #SET TO FALSE to use without lists
    clearOut = True # SET TO FALSE to keep all previous scripts written

    if not os.path.isdir(path):
        print(f"Directory not found: {path}")
    else:
        if clearOut:
            clearOutputFile(outputFile)
        if isList: #LIST COMBINING
            scripts = []
            scripts = combineLst(path, scripts)
            
            if not scripts: #empty checking
                print(f"{outputFile} is empty")
            else:
                writeScript(scripts, outputFile) #writes list to output file
                print(f"Combined scripts into {outputFile}")
            
            # for script in scripts:
            #     print(f"Script from {script['filePath']}:") #prints file path
            #     print(script['content']) # prints content of script
            #     print("\n")
        else:
            combineScripts(path, outputFile)
            
            if os.path.getsize(outputFile) == 0:
                print(f"{outputFile} is empty")
            else:
                print(f"Combined scripts into {outputFile}")
