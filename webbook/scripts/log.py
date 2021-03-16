def fatal(pClass, pMessage):
    print(f"FATAL in {pClass} : {pMessage}")
    print("----------------------------")
    exit(1)
    return False

def error(pClass, pMessage):
    print(f"ERROR in {pClass} : {pMessage}")
    return False

def warning(pClass, pMessage):
    print(f"WARNING in {pClass} : {pMessage}")

def info(pMessage):
    print(f"INFO : {pMessage}")

def debug(pClass, pFunction, pMessage):
    print(f"DEBUG : {pClass} - {pFunction} {pMessage}")
