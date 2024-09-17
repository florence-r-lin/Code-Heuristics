from HardMetrics import HardMetrics
from os import listdir
from os.path import isfile, join
import csv

onlyfiles = [f for f in listdir("studentScripts")]
onlyfiles = [join("studentscripts/", f) for f in onlyfiles]
print(onlyfiles)
for i in onlyfiles:
     print(HardMetrics(i))