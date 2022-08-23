import sys

gpus = sys.argv[1]

with open('test.txt', 'w') as f:
    f.write(gpus)
