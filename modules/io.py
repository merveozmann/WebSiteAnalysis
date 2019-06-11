def read(filename):
    result = []
    file = open("..\\data\\" + filename + ".csv"  , "r")
    for line in file:
        line = line.split(",")
        result.append(line)


def write(data, filename):
    file = open("..\\data\\" + filename + ".csv", "a")
    for line in data:
        file.write(line)
