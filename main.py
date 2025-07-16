from src import jsonReader
import sys

if __name__ == '__main__':
    argv = sys.argv
    if (len(argv) == 2):
        print(jsonReader.jsonReader(argv[1]))
