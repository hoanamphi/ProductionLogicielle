import sys
import csv

with open('data/installations.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)
print(sys.version)