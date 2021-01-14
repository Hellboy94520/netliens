def fatal(pClass, pMessage):
    print("FATAL in {} : {}\n".format(pClass, pMessage))
    print("----------------------------")
    exit(1)
    return False

def error(pClass, pMessage):
    print("ERROR in {} : {}\n".format(pClass, pMessage))
    return False

def warning(pClass, pMessage):
    print("WARNING in {} : {}\n".format(pClass, pMessage))

def info(pMessage):
    print("INFO : {} \n".format(pMessage))
