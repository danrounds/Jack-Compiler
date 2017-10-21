global uniqueIfIdentifier, uniqueWhileIdentifier # Integers
'''Used to provide unique IDs for ifs/whiles in code output'''
def getIfID():
    # global parsenum, uniqueIfIdentifier
    # if parsenum == 2:
    #     uniqueIfIdentifier += 1
    #     return str(uniqueIfIdentifier)
    # return str()

    global parsenum, uniqueIfIdentifier
    uniqueIfIdentifier += 1
    return str(uniqueIfIdentifier)


def getWhileID():
    # global parsenum, uniqueWhileIdentifier
    # if parsenum == 2:
    #     uniqueWhileIdentifier += 1
    #     return str(uniqueWhileIdentifier)
    # return str()

    global parsenum, uniqueWhileIdentifier
    uniqueWhileIdentifier += 1
    return str(uniqueWhileIdentifier)

def init():
    global uniqueIfIdentifier, uniqueWhileIdentifier
    uniqueIfIdentifier = uniqueWhileIdentifier = -1



