import time
import os
import sys
from IO.template_reader import *
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
    global TAGS, SEPARATOR  # get global variables from config
    for row in plan:  # loop thru plan by rows
        splitted_row = row.split(SEPARATOR)  # split row to list 
        print("ROW :",splitted_row)  # control print 
        links = splitted_row[1:] # get rid of symbol from last link
        if len(splitted_row) > 1:  # if more then 1 
            data = prepare_data(splitted_row[0], prepare_multiple_links(links), TAGS)
        filename = splitted_row[0] + '.md'
        print(filename)  # control print created filename
        # check if file already exists
        if filename_exists(filename, index_of_files) is True:
            print("FILE ALREADY EXISTS")
        elif filename_exists(filename,index_of_files) is False:
            write_md(filename=filename, data=data)  # if file is new write him down
            print("SAVED", filename)  # control print 
    return True
    


if __name__ == "__main__":

    """ 
    M A I N   P R O G R A M M - U N D E R   D E V E L O P M E N T
    
    """
    print(SEPARATOR, TAGS, END_SYMBOL)  # Control print

    # check if file was passed as argument via CLI
    if len(sys.argv) == 1:
        print("NO FILE ARGUMENT")
    else:
        filename = sys.argv[1]

    # READ FILE CONTAINING PLAN
    try:
        plan = read_plan(filename=PLANFILE)  # use function read plan from IO.io_plan
    except FileNotFoundError:
        plan = []
        print("PLAN FILE DOESN'T EXIST")
        # TODO Make a New Plan File
    finally:
        # TODO Log if plan file was successfully loaded
        pass
    
    # get index of existing Markdown files
    index_of_files = get_index()  # use function get_index from IO.io_plan
    print(index_of_files)  # control print all collected Markdown files
    
    #check if doesnt contain duplicity
    a = duplicity_check_plan(plan)  # TODO Does'nt work
    print(a)

    # save prepared data to files
    prepare_data_2_save(plan, index_of_files)  #  reads row from plan and generates Markdown file

    a = prepare_multiple_links(["hallo", "hallo"])
    print(a)

    print(sys.argv)  # control print all arguments passed via CLI

    
    """

    file = os.getcwd()+"/templates/template"  # variable file is defined as file from templates folder
    print(file)  # control print
    obj = TemplateReader(filename=file)  # defines instance of TemplateReader class
    obj.read_template() # read template from template file
    print(obj.rows)  # control print instance rows as dictionary
    print(obj.tags)  # 
    print(len(obj.rows))
    obj.purge_last30blankrows()
    obj.seek_tags_and_links()
    print(obj.rows)
    print(len(obj.rows.keys()))

    """

    


    
    

