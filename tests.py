import unittest
from sudoku import SudokuCell, Sudoku

class TestSudokuCellMethods(unittest.TestCase):

	def test_init(self):
		test_cell = SudokuCell(3, 4)
		self.assertFalse(test_cell.value)
		self.assertEqual(test_cell.valid_numbers, range(1, 10))

	def test_box_coordinates(self):
		test_cell = SudokuCell(1, 1)
		test_values = [(a+1, b) for a, b in enumerate([1, 1, 1, 2, 2, 2, 3, 3, 3])]
		for input_coord, box_coord in test_values:
			self.assertEqual(box_coord, test_cell.return_box_coord(input_coord))

	def test_coordinate_generation(self):
		test_values = [[(1, 1), (1, 1, 1)],
						[(1, 4), (1, 4, 4)],
						[(4, 7), (4, 7, 8)],
						[(7, 4), (7, 4, 6)],
						[(9, 9), (9, 9, 9)]]

		for (x, y), output_coords in test_values:
			test_cell = SudokuCell(x, y)
			self.assertEqual(test_cell.get_coordinates(x, y), output_coords)

	def test_invalidate_number(self):
		test_cell = SudokuCell(1, 1)
		test_values = [1, 2, 3, 5, 6, 7, 8, 9]
		test_cell.invalidate_number(4)
		self.assertEqual(test_cell.valid_numbers, test_values)

	def test_pick_value(self):
		test_values = range(1, 10)
		test_cell = SudokuCell(1, 1)
		test_cell.pick_value()
		self.assertTrue(test_cell.value in test_values)

	def additional_tests(self):
		more_test_values = [1, 2, 5, 7, 9]
		test_cell = SudokuCell(1, 1)
		for num in [3, 4, 6, 8]:
			test_cell.invalidate_number(num)
		test_cell.pick_value()
		self.assertTrue(test_cell.value in more_test_values)

class TestSudokuMethods(unittest.TestCase):

	def test_init(self):
		test_grid = Sudoku()
		self.assertEqual(len(test_grid.cells), 81)
		for cell in test_grid.cells:
			self.assertTrue(cell.coordinates[0] in range(1, 10))
			self.assertTrue(cell.coordinates[1] in range(1, 10))
			self.assertTrue(cell.coordinates[2] in range(1, 10))

		self.assertEqual(test_grid.lowest_valid_numbers, 9)

	def test_invalidate_numbers_in_other_cells(self):
		test_grid = Sudoku()
		set_cell = test_grid.cells[0]
		set_cell.value = 1
		set_cell.valid_numbers = [1]
		test_grid.invalidate_numbers_in_other_cells(set_cell)
		for other_cell in test_grid.cells:
			if any([coord_this == coord_other for (coord_this, coord_other) in zip(set_cell.coordinates, other_cell.coordinates)]) and not other_cell.value:
				self.assertFalse(1 in other_cell.valid_numbers)
			else:
				self.assertTrue(1 in other_cell.valid_numbers)

	def test_determine_lowest_valid_numbers(self):
		test_grid = Sudoku()
		counter = 0
		
		for cell in test_grid.cells:
			if counter % 2 == 0:
				cell.valid_numbers = [1, 2, 3, 4, 5]
			else:
				cell.value = 1
				cell.valid_numbers = [1]
			counter += 1
		
		test_grid.determine_lowest_valid_numbers()
		self.assertEqual(test_grid.lowest_valid_numbers, 5)

	def test_generate_cell(self):
		test_grid = Sudoku()
		for n in range(len(test_grid.cells)):
			candidate_cell = next(cell for cell in test_grid.cells if (len(cell.valid_numbers) == test_grid.lowest_valid_numbers and not cell.value))
			test_grid.generate_cell()
			self.assertTrue(candidate_cell.value in range(1, 10))
			self.assertEqual(candidate_cell.valid_numbers, [candidate_cell.value])

	def test_generate_full(self):
		test_grid = Sudoku()
		test_grid.generate_full()
		for coord in range(1, 10):
			x_rows = sorted([cell.value for cell in test_grid.cells if cell.coordinates[0] == coord])
			y_cols = sorted([cell.value for cell in test_grid.cells if cell.coordinates[1] == coord])
			z_boxes = sorted([cell.value for cell in test_grid.cells if cell.coordinates[2] == coord])
			self.assertEqual(x_rows, range(1, 10))
			self.assertEqual(y_cols, range(1, 10))
			self.assertEqual(z_boxes, range(1, 10))

if __name__=="__main__":
	unittest.main()