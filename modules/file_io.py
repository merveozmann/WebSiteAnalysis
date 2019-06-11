def read(filename):
    result = []
    file = open("data\\" + filename + ".csv"  , "r", encoding="utf-8")
    for line in file:
        line = line.strip("\n")
        result.append(line)

    return result


def write(data, filename):
    file = open("data\\" + filename + ".csv", "w", encoding="utf-8")
    for line in data:
        file.write(str(line) + "\n")


def parse_domains():
        data = read("data_raw")
        dom = []
        for d in data:
                if (d.startswith("http://")):
                        d = d[7:]
                elif (d.startswith("https://")):
                        d= d[8:]
                domain = d.split('/')[0].lower()

                if(domain not in dom):
                        dom.append(domain)
        return dom

def parse_blacklist():
        data = read("blacklist")
        dom = []
        for d in data:
                d = d.split(',')[1]

                if (d.startswith("http://")):
                        d = d[7:]
                elif (d.startswith("https://")):
                        d = d[8:]
                domain = d.split('/')[0].lower()

                if(domain not in dom):
                        dom.append(domain)


        return dom