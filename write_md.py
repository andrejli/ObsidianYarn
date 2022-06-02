import time
import os

# config
global SEPARATOR, END_SYMBOL
SEPARATOR = "\t"
END_SYMBOL = "<>\n"


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
            if row == END_SYMBOL:
                break   # defined end 
            else:
                result.append(row)
    print(result)
    return result


def add_link(link: str):
    """
    function add link to string of links in markdown file. If first character 
    is # then leave it for further processing
    param1::: link - string represention of Zettelkasten link
    return::: prepared link string [[ ]] 
    """
    return "[[" + link + "]]"


def prepare_multiple_links(links: list):
    """

    """
    result = str()
    for i in links:
        if i[-1] == "\n":
            i = i[:-1]
        result += " " + add_link(i)
    print(result)
    return result


def duplicity_check(plan: list, index: list):  # TODO DOesnt work
    """
    function checks plan file and index of file if there is not duplicity
    in nodes or files.
    param1::: plan - list of node names with links
    param2::: index - list of all files in Zettelkasten directory
    return::: Boolean value if DUPLICITY Exists
    """
    nodes = []
    for i in plan:
        node = i.split(SEPARATOR)
        nodes.append(node[0])
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
        

def get_index(path=None):
    """
    function makes index of all .md files in directory and throws them to
    list.
    param1::: path - string contains path to look after Markdown files
    return::: result - list of all markdown files
    """
    if path is None:
        path = os.getcwd()
    print("PATH :", path)
    content = os.listdir()
    result = []
    for i in content:
        print(i)
        if i[-3:] == '.md':
            result.append(i)
    print(result)
    return result


def prepare_data(name: str, links: str):
    """
    function prepares data to simple template of markdown file.
    param1::: name - string represents name of Markdown Note
    param2::: link - string represents link to another note
    return::: prepared string
    """ 
    # TODO In future there will data from plan should be parsed and put into specified template from templates directory. 
    result = "# "
    result += name + "\n\n"  
    # TODO check if not tag example #topic
    result += "## Links "+ links
    result += "\n\nCreated by SCRIPT"
    return result


def filename_exists(filename: str, index: list):
    """
    Function checks if file already exists
    param1::: filename - String representation which contains path and file
    param2::: index of files in directory
    return::: Boolean value True if file already exists
    """
    if filename in index_of_files:
        return True
    else:
        return False


def write_md(filename, data):  # TODO Move to IO 
    """
    Simple function takes filename and prepared data and saves them to Markdown file.
    param1::: filename - string with path and filename
    param2::: data - String prepared 
    return::: Boolean status if data was saved
    """
    with open(file=filename, mode="w", encoding="utf8") as f:
        f.write(data)
        print("SAVED")
        return True


def prepare_data_2_save(plan, index):
    """
    Function iterates thru plan and prepare values to write to files. 
    First value in plan is NAME of markdown file, other value is LINK
    """
    for row in plan:
        splitted_row = row.split(SEPARATOR)
        print("ROW :",splitted_row)
        links = splitted_row[1:] # get rid of symbol from last link
        if len(splitted_row) > 1:
            data = prepare_data(splitted_row[0], prepare_multiple_links(links))
        filename = splitted_row[0] + '.md'
        print(filename)
    	# check if file already exists
        if filename_exists(filename, index_of_files) is True:
    	    print("FILE ALREADY EXISTS")
        elif filename_exists(filename,index_of_files) is False:
    	    write_md(filename=filename, data=data)
    	    print("SAVED", filename)
    return True
    


if __name__ == "__main__":
    # READ FILE CONTAINING PLAN
    try:
        plan = read_plan(filename="plan.txt")
    except FileNotFoundError:
        plan = []
        print("PLAN FILE DOESN'T EXIST")
    finally:
        pass
    
    # get index of existing Markdown files
    index_of_files = get_index()
    print(index_of_files)
    
    #check if doesnt contain duplicity
    # duplicity_check(plan, index_of_files)

    # save prepared data to files
    prepare_data_2_save(plan, index_of_files)

    # a = prepare_multiple_links(["hallo", "hallo"])
    # print(a)


    
    

