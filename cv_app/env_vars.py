# Parsing txt file for extracting variables
def parse_file(name):
    variables = dict()
    for i in open(name):
        name = i.split('=')[0][0:-1]
        var = i.split('=')[1].rstrip()[2:-1]
        variables[name] = var
    return variables
