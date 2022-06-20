import os
from IO.io_plan import read_plan

def test_read_plan():
	file = os.getcwd()+"/tests/test_plan"
	assert read_plan(file) == ['Alpha\n', 'Beta\n', 'Gama\n', 'Delta\n']
