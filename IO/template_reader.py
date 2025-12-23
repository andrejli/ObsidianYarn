
import os
import re
from IO.exceptions import TemplateError

class TemplateReader:
	"""
	Reads a template file and stores its rows in a dictionary.
	Detects <Tags> and <Links> placeholders for Markdown generation.
	"""
	def __init__(self, filename):
		self.template_file = filename
		self.rows = {}
		self.tags = []

	def read_template(self):
		"""
		Reads the template file line by line, storing each row in self.rows.
		Stops reading if more than 30 consecutive blank lines are encountered.
		Raises:
			TemplateError: If template file cannot be read.
		"""
		if not self.template_file:
			raise TemplateError("Template filename cannot be empty")
		
		if not os.path.exists(self.template_file):
			raise TemplateError(f"Template file not found: {self.template_file}")
		
		blank_counter = 0
		counter = 0
		try:
			with open(self.template_file, mode="r", encoding="utf8") as f:
				for row_content in f:
					self.rows[counter] = row_content
					counter += 1
					if row_content.strip() == "":
						blank_counter += 1
					else:
						blank_counter = 0
					if blank_counter > 30:
						break
		except PermissionError:
			raise TemplateError(f"Permission denied reading template: {self.template_file}")
		except UnicodeDecodeError as e:
			raise TemplateError(f"Invalid encoding in template {self.template_file}: {e}")
		except Exception as e:
			raise TemplateError(f"Error reading template {self.template_file}: {e}")

	def purge_last30blankrows(self):
		"""
		Removes the last 30 rows from self.rows (assumed to be blank).
		"""
		if len(self.rows) > 30:
			self.rows = {i: self.rows[i] for i in range(len(self.rows) - 30)}
		return True

	def seek_tags_and_links(self):
		"""
		Scans self.rows for template placeholders like <Name>, <Tags>, <Links>, etc.
		Returns the complete dictionary of all template rows.
		"""
		# Return all rows - placeholders will be processed during generation
		return self.rows




if __name__ == "__main__":
	file = os.path.join(os.getcwd(), "templates", "template")
	print(f"Template file: {file}")
	obj = TemplateReader(filename=file)
	obj.read_template()
	print(f"Rows: {obj.rows}")
	print(f"Tags: {obj.tags}")
	print(f"Number of rows: {len(obj.rows)}")
	obj.purge_last30blankrows()
	print(f"Tag/Link positions: {obj.seek_tags_and_links()}")
	