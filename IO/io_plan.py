
END_SYMBOL = ""

def read_plan(filename):
    """
    function reads file which contains objects to transfer to .md files
    Objects are separated by special character and ended with 
    If function detect <> means end of file.
    param1::: filename contains string with file containing plan
    return::: list of all related objects
    """
    result = list()
    with open(file=filename, mode="r", encoding="utf8") as f:
        while True:
            row = f.readline()
            print(row)
            if row == "<>\n":
                break   # defined end 
            else:
                result.append(row)
    print(result)
    return result