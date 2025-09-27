
import os
import pytest
from IO.io_plan import read_plan, duplicity_check_plan, file_is_markdown, get_index, filename_exists
def test_filename_exists():
	index = ["test_plan"]  # MOCK index of files
	plan_file = "test_plan"  # plan file without PATH
	assert filename_exists(plan_file, index) is True
from IO.template_reader import TemplateReader

TESTS_DIR = os.path.join(os.getcwd(), "tests")
TEMPLATES_DIR = os.path.join(os.getcwd(), "templates")

def test_read_plan():
	file = os.path.join(TESTS_DIR, "test_plan")
	assert read_plan(file) == ['Alpha\n', 'Beta\n', 'Beta\n', 'Gama\n', 'Delta\n']

def test_duplicity_plan():
	file = os.path.join(TESTS_DIR, "test_plan")
	plan = read_plan(file)
	assert duplicity_check_plan(plan) is True

def test_TR_instance():
	file = os.path.join(TEMPLATES_DIR, "template")
	obj = TemplateReader(filename=file)
	assert isinstance(obj, TemplateReader)

def test_template_rows():
	file = os.path.join(TEMPLATES_DIR, "template")
	obj = TemplateReader(filename=file)
	obj.read_template()
	assert isinstance(obj.rows, dict)

def test_file_is_markdown():
	path_md = os.path.join(TESTS_DIR, "test.md")
	path_plan = os.path.join(TESTS_DIR, "test_plan")
	assert file_is_markdown(path=path_md) is True
	assert file_is_markdown(path=path_plan) is False

def test_get_index():
	files = get_index(TESTS_DIR)
	assert "test.md" in files

def test_filename_exists():
	index = ["test_plan"]  # MOCK index of files !!! 
	plan_file = "test_plan"  # plan file without PATH !!! 
	assert filename_exists(plan_file, index) == True

