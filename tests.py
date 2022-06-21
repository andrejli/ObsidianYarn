import os
from IO.io_plan import read_plan
from IO.template_reader import TemplateReader

def test_read_plan():
	file = os.getcwd()+"/tests/test_plan"
	assert read_plan(file) == ['Alpha\n', 'Beta\n', 'Gama\n', 'Delta\n']

def test_TR_instance():
	obj = TemplateReader(filename="template")
	assert isinstance(obj, TemplateReader) == True
