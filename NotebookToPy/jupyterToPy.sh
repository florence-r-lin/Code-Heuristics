currDic="$(pwd)/*" #This is meant to be the file path of the folder containing ipynb files
for file in $currDic
do
    jupytext --to py $file
done