import os
from IO.io_plan import *
from IO.template_reader import TemplateReader

# P L A N   T E S T S

def test_read_plan():
	file = os.getcwd()+"/tests/test_plan"
	assert read_plan(file) == ['Alpha\n', 'Beta\n', 'Beta\n', 'Gama\n', 'Delta\n']

def test_duplicity_plan():
	file = os.getcwd()+"/tests/test_plan"  # TODO LETs CHECK AGAIN
	a = duplicity_check_plan(plan=file)
	assert a == True

def test_TR_instance():
	obj = TemplateReader(filename="template")
	assert isinstance(obj, TemplateReader) == True

def test_template_rows():
	file = os.getcwd()+"/templates/template"
	obj = TemplateReader(filename=file)
	assert obj.rows == dict()
	# TODO Do More test on template reader

def test_file_is_markdown():
	PATH = os.getcwd() + "/tests/test.md"
	assert file_is_markdown(path=PATH) == True
	PATH = os.getcwd() + "/tests/test_plan"
	assert file_is_markdown(path=PATH) == False


def test_get_index():
	PATH = os.getcwd() + "/tests/"
	assert get_index(PATH) == ["test.md"]

def test_filename_exists():
	index = ["test_plan"]  # MOCK index of files !!! 
	plan_file = "test_plan"  # plan file without PATH !!! 
	assert filename_exists(plan_file, index) == True

