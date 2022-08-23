import sys

gpus = sys.argv[1]

with open('brand.txt', 'w') as f:
    f.write(gpus)
