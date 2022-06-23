import os
from IO.io_plan import *
from IO.template_reader import TemplateReader

def test_read_plan():
	file = os.getcwd()+"/tests/test_plan"
	assert read_plan(file) == ['Alpha\n', 'Beta\n', 'Gama\n', 'Delta\n']

def test_TR_instance():
	obj = TemplateReader(filename="template")
	assert isinstance(obj, TemplateReader) == True

def test_get_index():
	PATH = os.getcwd() + "/tests/"
	assert get_index(PATH) == ["test.md"]

def test_filename_exists():
	index = ["test_plan"]  # MOCK index of files !!! 
	plan_file = "test_plan"  # plan file without PATH !!! 
	assert filename_exists(plan_file, index) == True

