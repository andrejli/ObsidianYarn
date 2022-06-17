

import re

class TemplateReader(object):

	def __init__(self, filename):
		self.template_file = filename
		self.rows = dict()
		self.tags = list()

	def read_template(self):
		blank_counter = 0
		counter = 0
		with open(file=self.template_file, mode="r", encoding="utf8") as f:
			while True:
				row_content = f.readline()
				self.rows[counter] = row_content
				counter += 1
				if row_content == "":
					blank_counter += 1
				else:
					blank_counter = 0

				if blank_counter > 30:
					return True
				print(row_content)

				
	def purge_last30blankrows(self):
		result = dict()
		for i in range(0, len(self.rows)-30):
			result[i] = self.rows[i]
			print(result[i])
		self.rows = result
		return True


	def seek_tags_and_links(self): # TODO Both Tags and Links can not be in One Row
		for i in range(0,len(self.rows)):
			
			hit = re.search(r'(<[A-Z])\w+>', self.rows[i])
			try:
				print(hit.group(0))
				print(hit.span())
				if hit.group(0) == '<Tags>':
					print("FOUND TAGS")
				if hit.group(0) == '<Links>':
					print("FOUND LINKS")
			except AttributeError:
				print("NONE")
			finally:
				pass



if __name__ == "__main__":
	obj = TemplateReader(filename="template")
	obj.read_template()
	print(obj.rows)
	print(obj.tags)
	print(len(obj.rows))
	obj.purge_last30blankrows()
	obj.seek_tags_and_links()