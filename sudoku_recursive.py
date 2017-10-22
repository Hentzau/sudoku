import random

class SudokuCell(object):
	def __init__(self, x, y, n):
		self.coordinates = self.get_coordinates(x, y)
		self.value = None

	def return_box_coord(self, coord):
		coord = coord - 1
		return coord // 3 + 1

	def get_coordinates(self, x, y):
		box_x_coord = self.return_box_coord(x)
		box_y_coord = self.return_box_coord(y)
		box_num = box_x_coord + (box_y_coord - 1) * 3
		return (x, y, box_num)

	def set_value(self, value):
		self.value = value

class SudokuGrid(object):
	def __init__(self, n):
		self.cells = []
		self.n = n
		for x in range(1, n**2+1):
			for y in range(1, n**2+1):
				self.cells.append(SudokuCell(x, y, n))

	def get_check_values(self, check_cell):
		return [cell.value for cell in self.cells if (any([coord_this == coord_other for (coord_this, coord_other) in zip(check_cell.coordinates, cell.coordinates)]) 
															and not cell.coordinates == check_cell.coordinates) ]
		# check_values = []
		# for cell in self.cells:
		# 	if (any([coord_this == coord_other for (coord_this, coord_other) in zip(check_cell.coordinates, cell.coordinates)]) and not cell.coordinates == check_cell.coordinates):
		# 		check_values.append(cell.value)
		# 		print check_values

		# return check_values

	def solve_for_depth(self, depth):

		# basic method based on Gareth Rees' answer to https://codereview.stackexchange.com/questions/88849/sudoku-puzzle-generator
		# which I found when my previous brute-force method had a 25% failure rate and I started wondering if there was a way
		# to try different potential cell values via recursion without tossing out the entire grid and starting again.

		def recursive_solve(position, depth=depth):
			# Identify candidate cell for solve based on index.
			candidate_cell = self.cells[position]
			# Find cells in same row, column and box and decant all their current values into a list
			check_cell_values = self.get_check_values(candidate_cell)
			# Generate and randomise a list of possible values for the candidate cell
			possible_values = range(1, self.n**2 + 1)
			random.shuffle(possible_values)
			# Test possible values one at a time
			for value in possible_values:
                # Check if the current value is already in the check values list (and hence invalid)
				if value not in check_cell_values:
					# If not, set this cell value to the current possible value
					candidate_cell.set_value(value)
					# Then, check that when run again, recursive_solve provides a valid answer to the next candidate cell in the cells list
					# This run of recursive_solve will perform the same check and call recursive_solve on the *next* cell in the list after that one, and it will continue to do so recursively
					# The recursion is ended when either of the following conditions are true:
					# 1) recursive_solve hits a dead end and can't complete the grid (in which case it returns False as below).
					# In this event the recursion chain will return False, backtrack one cell/recursion step and try other possible answers. 
					# If those answers also dead-end, it'll backtrack one further cell and try other possible answers. And so on back up the chain until it finds a viable route forward again.
					# 2) is if the end of the list of cells is reached, in which case the below statement will *not* trigger recursive_solve on that iteration and will immediately return True
					# key thing to understand is that this statement won't return True until the entire grid has been solved - when it hits this point it's just building out solution paths 
					# until it finds one that works
					if position + 1 == depth or recursive_solve(position + 1):
						return True
			# If all possible values are checked (both in this step and in subsequent recursion steps) without valid solutions being found, this branch is a dead-end
			# Reset the cell value so that other solutions may be attempted.
			candidate_cell.value = None
			# Then return False to terminate this recursion branch
			return False

		recursive_solve(0)

	def full_solve(self):
		self.solve_for_depth(len(self.cells))

	def check(self):
		for cell in self.cells:
			if cell.value in self.get_check_values(cell):
				print 'Invalid solution for cell %s' % cell.coordinates
				return

		print 'Solution A-OK'


	def display(self):
		for y in range(1, 10):
			row = []
			for x in range(1, 10):
				nextval = next(cell.value for cell in self.cells if (cell.coordinates[0] == x and cell.coordinates[1] == y))
				row.append(nextval)
			print row

if __name__=="__main__":
	grid = SudokuGrid(3)
	grid.full_solve()
	grid.display()
	grid.check()

	partial_grid = SudokuGrid(3)
	partial_grid.solve_for_depth(40)
	partial_grid.display()
