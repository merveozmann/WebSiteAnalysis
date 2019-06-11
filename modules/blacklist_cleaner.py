def read(filename):
    result = []
    file = open("..\\data\\" + filename + ".csv"  , "r")
    for line in file:
        line = line.strip("\n")
        result.append(line)

    return result

def clean():
    blacklist = read("blacklist")
    blacklist_clean = []
    safe = []
    for b in blacklist:
        b = b.split(',')
        blacklist_clean.append(b[1])
        safe.append(b[2])
    
    return blacklist_clean, safe