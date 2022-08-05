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

    WARNING If link is tag like #python will be automatically put into 
    global variable TAGS.
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



def read_template(filename: str):
    """
    Function reads template and stores ROWS into Dictionary. Then 
    Automatically finds predefined <tags> and put them separately.
    param1::: filename of template file in templates folder  # TODO Make It configurable
    return::: Dictionary containing all rows of template
    """
    result = dict()
    # TODO Check if template exists
    file = os.getcwd()+"/templates/"+filename
    print(file)
    obj = TemplateReader(filename=file)
    obj.read_template()
    print("ROWS:,",obj.rows)
    print("TAGS:",obj.tags) # prints out founded tags (links, author, tags)
    print("LENGTH OF TEMPLATE:",len(obj.rows))
    obj.purge_last30blankrows() # get rid of empty space 
    result = obj.seek_tags_and_links()
    print("FOUNDED TAGS:", result)
    return result


def prepare_data(name: str, links: str, tags: str):  # DEFAULT TEMPLATE
    """
    function prepares data to default template of markdown file.
    param1::: name - string represents name of Markdown Note
    param2::: link - string represents link to another note
    param3::: tags: Is overwritten by global variable TAGS
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
    """
    function prepares data for CUSTOM template saved in templates folder
    param1::: name - string represents name of Markdown Note
    param2::: link - string represents link to another note
    param3::: tags: Is overwritten by global variable TAGS
    return::: prepared string
    
    """
    global TAGS, AUTHOR
    tags = TAGS
    result = str()
    loaded_template=read_template(filename="template")
    print(loaded_template)
    for i in loaded_template:
        # print("ROW CONTENT :", i, loaded_template[i]) # control print
        if "<Name>" in loaded_template[i]:
            result += "# "+ name + "\n"
            continue
        if "<Tags>" in loaded_template[i]:
            result += "## TAGS :"+ tags + "\n"
            continue
        if "Links" in loaded_template[i]:
            result += "## LINKS : "+ links + "\n"
            continue
        if "<Author>" in loaded_template[i]:
            result += "### Was Created By : "+ AUTHOR + "\n"
            continue
        if "<Date>" in loaded_template[i]:
            date = time.strftime("%d.%m.%Y %H:%M")
            result += "### Date : "+ date + "\n"
            continue
        else:
            result += loaded_template[i]

    return result


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
            data = prepare_data_custom(splitted_row[0], prepare_multiple_links(links), TAGS)
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
    print(SEPARATOR, TAGS, END_SYMBOL, AUTHOR)  # Control print

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

    a = prepare_data_custom(name="# Andrea", links= "[[Hello]]", tags="#python")
    print(a)

    """

    

    


    
    

