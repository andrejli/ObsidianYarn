import time
import os
import sys
from IO.io_plan import *
from configs.config import *
# config








def add_link(link: str): # TODO move to CORE
    """
    function add link to string of links in markdown file. If first character 
    is # then leave it for further processing
    param1::: link - string represention of Zettelkasten link
    return::: prepared link string [[ ]] 
    """
    global TAGS
    if link[0] == "#": # support for TAGS
        TAGS += link + " "
        return ""
    else:
        return "[[" + link + "]]"


def prepare_multiple_links(links: list):  # TODO Move to CORE
    """
    function takes list of links and prepares string to write into markdown file
    param1::: links - list of links
    return::: result which contains string with all links prepared for Markdown template
    """
    result = str()
    for i in links:
        if i[-1] == "\n":
            i = i[:-1]
        result += " " + add_link(i)
    print(result)
    return result



        


"""
def read_template(filename: str):
    result = dict()
    with open(filename, mode="r", encoding="utf8" as f:

    pass
"""

def prepare_data(name: str, links: str, tags: str):  # DEFAULT TEMPLATE
    """
    function prepares data to simple template of markdown file.
    param1::: name - string represents name of Markdown Note
    param2::: link - string represents link to another note
    return::: prepared string
    """ 
    # TODO In future there will data from plan should be parsed and put into specified template from templates directory. 
    global TAGS
    tags = TAGS
    result = "# "
    result += name + "\n\n"  
    # TODO check if not tag example #topic
    result += "## Links "+ links
    result += "\n## Tags " + tags
    result += "\n\nCreated by SCRIPT"
    return result

def prepare_data_custom(name: str, links: str, tags: str):
    pass





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


def prepare_data_2_save(plan, index):  # TODO Move to CORE
    """
    Function iterates thru plan and prepare values to write to files. 
    First value in plan is NAME of markdown file, other value is LINK
    """
    global TAGS, SEPARATOR
    for row in plan:
        splitted_row = row.split(SEPARATOR)
        print("ROW :",splitted_row)
        links = splitted_row[1:] # get rid of symbol from last link
        if len(splitted_row) > 1:
            data = prepare_data(splitted_row[0], prepare_multiple_links(links), TAGS)
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
    print(SEPARATOR, TAGS, END_SYMBOL)

    # check if file was passed as argument
    if len(sys.argv) == 1:
        print("NO FILE ARGUMENT")
    else:
        filename = sys.argv[1]

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

    print(sys.argv)

    
    

