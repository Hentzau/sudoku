import random

class SudokuCell(object):
	def __init__(self, x, y):
		self.coordinates = self.get_coordinates(x, y)
		self.valid_numbers = range(1, 10)
		self.value = None

	def return_box_coord(self, coord):
		coord = coord - 1
		return coord // 3 + 1

	def get_coordinates(self, x, y):
		box_x_coord = self.return_box_coord(x)
		box_y_coord = self.return_box_coord(y)
		box_num = box_x_coord + (box_y_coord - 1) * 3
		return (x, y, box_num)

	def invalidate_number(self, n):
		self.valid_numbers = [num for num in self.valid_numbers if num != n]

	def pick_value(self):
		self.value = random.choice(self.valid_numbers)
		self.valid_numbers = [self.value]

class Sudoku(object):
	def __init__(self):
		self.cells = []
		for x in range(1, 10):
			for y in range(1, 10):
				self.cells.append(SudokuCell(x, y))
		self.lowest_valid_numbers = 9

	def invalidate_numbers_in_other_cells(self, this_cell):
		for other_cell in self.cells:
			if any([coord_this == coord_other for (coord_this, coord_other) in zip(this_cell.coordinates, other_cell.coordinates)]) and not other_cell.value:
				other_cell.invalidate_number(this_cell.value)
				self.determine_lowest_valid_numbers()

	def determine_lowest_valid_numbers(self):
		self.lowest_valid_numbers = min([len(cell.valid_numbers) for cell in self.cells if not cell.value])

	def generate_cell(self):
		candidate_cell = next(cell for cell in self.cells if (len(cell.valid_numbers) == self.lowest_valid_numbers and not cell.value))
		candidate_cell.pick_value()
		self.invalidate_numbers_in_other_cells(candidate_cell)

	def generate_full(self):
		self.num_of_unset_cells = len([cell for cell in self.cells if not cell.value])
		while self.num_of_unset_cells > 0:
			self.determine_lowest_valid_numbers()
			self.generate_cell()
			self.num_of_unset_cells -= 1

	def display(self):
		for y in range(1, 10):
			row = []
			for x in range(1, 10):
				nextval = next(cell.value for cell in self.cells if (cell.coordinates[0] == x and cell.coordinates[1] == y))
				row.append(nextval)
			print row


if __name__=="__main__":
	# grid = Sudoku()
	# grid.generate_full()
	# grid.display()
	test_grid = Sudoku()
	set_cell = test_grid.cells[0]
	set_cell.value = 1
	test_grid.invalidate_numbers_in_other_cells(set_cell)
	for other_cell in test_grid.cells:
		if any([coord_this == coord_other for (coord_this, coord_other) in zip(set_cell.coordinates, other_cell.coordinates)]):
			if other_cell.valid_numbers != range(2, 10):
				print other_cell.coordinates
				print other_cell.valid_numbers
	import pdb; pdb.set_trace()









    