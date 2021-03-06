import os
from configs.config import SEPARATOR

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
        print(file_is_markdown(path=filename))
        while True:
            row = f.readline()
            print(row)
            if row == "<>\n":  # use defined END SYMBOL in config file
                break   # defined end 
            else:
                result.append(row)
    print(result)
    return result


def get_index(path=None):  # TODO Move to IO
    """
    function makes index of all .md files in directory and throws them to
    list.
    param1::: path - string contains path to look after Markdown files
    return::: result - list of all markdown files
    """
    if path is None:
        path = os.getcwd()
    print("PATH :", path)
    content = os.listdir(path)
    result = []
    for i in content:
        print(i)
        if i[-3:] == '.md':
            result.append(i)
    print(result)
    return result

def file_is_markdown(path: str):
    """
    function takes path with file and checks if it it markdown file
    param1::: path - string containing path and filename
    return::: Boolean - 
    """
    if path[-3:] == '.md':
        return True
    else:
        return False



def filename_exists(filename: str, index: list):  # TODO Move to IO
    """
    Function checks if file already exists
    param1::: filename - String representation which contains path and file
    param2::: index of files in directory
    return::: Boolean value True if file already exists
    """
    index_of_files = index
    if filename in index_of_files:
        return True
    else:
        return False


def duplicity_check_plan(plan: list):  # TODO DOesnt work
    """
    function checks plan file and index of file if there is not duplicity
    in nodes or files.
    param1::: plan - list of node names with links
    param2::: index - list of all files in Zettelkasten directory
    return::: Boolean value if DUPLICITY Exists
    """
    nodes = []
    for i in plan:
        node = i.split(SEPARATOR)  # splits row into list
        nodes.append(node[0])  # adds name (first value) from plan to nodes
    
    nodes_set = set(nodes)  # define new variable as set 
    if len(nodes) != len(nodes_set):  # if length of nodes is not same as nodes_set
        print("DUPLICITY IN PLAN DETECTED", len(nodes), len(nodes_set))
        return True

    else:
        print("DUPLICITY IN PLAN NOT DETECTED")
        return False
    '''
    for i in nodes:
        if nodes.count(i) > 1:
            print("PLAN DUPLICITY DETECTED IN NODE :", i)
            return True
        # 
        filename = str(i) + ".md"
        f = filename_exists(filename, index)
        if f is True:
            print("FILE DUPLICITY DETECTED IN NODE :", i)
            return True
    return False
    '''