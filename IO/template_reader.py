
class TemplateReader(object):

	def __init__(self, filename):
		self.template_file = filename
		self.rows = dict()
		self.tags = list()

	def read_template(self):
		counter = 0
		with open(file=self.template_file, mode="r", encoding="utf8") as f:
			while True:
				row_content = f.readline()
				self.rows[counter] = row_content
				counter += 1
				if row_content == "<>\n":
					print(self.rows)
					return True


if __name__ == "__main__":
	obj = TemplateReader(filename="plan.txt")
	obj.read_template()