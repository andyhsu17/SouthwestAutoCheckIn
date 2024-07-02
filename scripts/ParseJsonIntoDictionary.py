textfile = 'text.txt'
outfile = 'out.txt'
def GetContentsInQuotes(line):
    start_index = line.find(':')
    if start_index == -1:
        print("unable to find semicolon")
        return
    start_index += 3 # to get to the first letter in quotes
    end_index = line.rfind('\"')
    return line[start_index : end_index]

out = open(outfile, "w")

with open(textfile, 'r') as file:
    for line in file.readlines():
        if line.startswith('{') or line.startswith('}'):
            continue
        if line.find('name') != -1:
            name = GetContentsInQuotes(line)
        elif line.find('value') != -1:
            value = GetContentsInQuotes(line)
            out.write(f'\"{name}\" : \"{value}\",\n')

out.close()
        


