import random

class SudokuCell(object):
	'''
	As I want to do something slightly more complicated than just storing the numbers in a list of list, it's a good
	idea to make a dedicated SudokuCell class so that I can set and store attributes on the cell level. Most important
	are the xyz cell coordinates, which are generated on instantiation based on x and y input.
	'''
	def __init__(self, x, y):
		# generate box coordinate and add all coordinates to coordinates attribute. A box is a discrete 3x3 slice of cells.
		self.coordinates = self.get_coordinates(x, y)
		# value is the true value of the cell. This will be hidden from the user by default and is used to store the solution.
		self.value = None
		# public_value is the cell value that the user can see.
		self.public_value = '-'

	def return_box_coord(self, coord):
		'''coord is the x or y coordinate for a cell (1-9 on a standard sudoku grid). This function returns the 
		corresponding box coordinate - so the 7th cell across the first row will be in the 3rd box across, and the 5th
		cell down a column will be in the 2nd box down.'''
		coord = coord - 1
		return coord // 3 + 1

	def get_coordinates(self, x, y):
		'''Take the x and y coordinates, convert them to box coordinates, and convert them to a box number where
		the 1st box is in the top left, and they are counted incrementally from left to right in rows.
        1 2 3
        4 5 6
        7 8 9
		'''
		box_x_coord = self.return_box_coord(x)
		box_y_coord = self.return_box_coord(y)
		box_num = box_x_coord + (box_y_coord - 1) * 3
		return (x, y, box_num)

	def set_value(self, value):
		'''Set the true cell value'''
		self.value = value

	def make_visible(self):
		'''Make the true cell value visible to the user by setting it to the public value'''
		self.public_value = self.value

	def set_public_value(self, value):
		'''Set the public value - this does not have to match the true value'''
		self.public_value = value

class SudokuGrid(object):
	'''Sudoku Grid class. It's a collection of SudokuCell objects stored in a one-dimensional list for easy iteration.
	If a specific cell needs to be looked up it can be found via its coordinates property. This class has methods
	for generating a random solution for the grid and displaying it, as well as some crude interactive functions so 
	that the user can try to solve the sudoku themselves.
	'''
	def __init__(self, n):
		self.cells = []
		self.n = n
		for x in range(1, n**2+1):
			for y in range(1, n**2+1):
				self.cells.append(SudokuCell(x, y, n))

	def get_check_values(self, check_cell):
		return [cell.value for cell in self.cells 
			if (any([coord_this == coord_other for (coord_this, coord_other) in zip(check_cell.coordinates, cell.coordinates)]) 
				and not cell.coordinates == check_cell.coordinates) ]

	def full_solve(self):
		'''
		Recursive solution for sudoku grid that's capable of backtracking and trying other paths if it hits a dead end.

		Basic method based on Gareth Rees' answer to https://codereview.stackexchange.com/questions/88849/sudoku-puzzle-generator
		which I found when my previous brute-force method had a 25% failure rate and I started wondering if there was a 
		way to try different potential cell values via recursion without tossing out the entire grid and starting again.
		'''

		def recursive_solve(position):
			# Identify candidate cell for solve based on index.
			candidate_cell = self.cells[position]
			# Find cells in same row, column and box and decant all their current values into a list
			check_cell_values = self.get_check_values(candidate_cell)
			if candidate_cell.value:
				possible_values = [candidate_cell.value]
			else:
				# Generate and randomise a list of possible values for the candidate cell
				possible_values = range(1, self.n**2 + 1)
				random.shuffle(possible_values)
				# Test possible values one at a time
			for value in possible_values:
                # Check if the current value is already in the check values list (and hence invalid)
				if value not in check_cell_values:
					# If not, set this cell value to the current possible value
					candidate_cell.set_value(value)
					'''
					Then, check that when run again, recursive_solve provides a valid answer to the next candidate 
					cell in the cells list. This run of recursive_solve will perform the same check and call 
					recursive_solve on the *next* cell in the list after that one, and it will continue to do so 
					recursively. The recursion is ended when either of the following conditions are true:

					1) recursive_solve hits a dead end and can't complete the grid (in which case it returns False as 
					below). In this event the recursion chain will return False, backtrack one cell/recursion step and 
					try other possible answers. If those answers also dead-end, it'll backtrack one further cell and 
					try other possible answers. And so on back up the chain until it finds a viable route forward again.

					2) is if the end of the list of cells is reached, in which case the below statement will *not* 
					trigger recursive_solve on that iteration and will immediately return True

					The key thing to understand is that this statement won't return True until the entire grid has been 
					solved - when it hits this point it's just building out solution paths until it finds one that works.
					'''
					if position + 1 == depth or recursive_solve(position + 1):
						return True
			# If all possible values are checked (both in this step and in subsequent recursion steps) without valid 
			# solutions being found, this branch is a dead-end. Reset the cell value so that other solutions may be 
			# attempted.
			candidate_cell.value = None
			# Then return False to terminate this recursion branch
			return False

		recursive_solve(0)


	def check(self):
		'''Simple sanity-check of solution validity. I don't expect this to ever be negative.'''
		for cell in self.cells:
			if cell.value in self.get_check_values(cell):
				print 'Invalid solution for cell %s' % cell.coordinates
				return
		print 'Solution A-OK'


	def display(self, public=True):
		'''
		Pretty-prints the sudoku grid complete with box and column separators. The public variable will print the 
		values known to the user if it's True, and the full hidden solution if it's False.
		'''
		template = '''|| {} | {} | {} || {} | {} | {} || {} | {} | {} ||'''
		separator = '''-----------------------------------------'''
		print separator
		for y in range(1, 10):
			row = []
			for x in range(1, 10):
				if public:
					nextval = next(cell.public_value for cell in self.cells if (cell.coordinates[0] == x 
																					and cell.coordinates[1] == y))
				else:
					nextval = next(cell.value for cell in self.cells if (cell.coordinates[0] == x 
																			and cell.coordinates[1] == y))
				row.append(nextval)
			print template.format(*row)
			if y % 3 == 0:
				print separator

	'''Some hacky code to interact with the grid on the command line - the idea is that a solution is generated,
	but the values are hidden from the user. They can input their own values, reveal x values as a sort of hint/seeding 
	system, or reveal the full solution if they're stuck. 

	No human being would ever use this, but then no human being who isn't me ever will. The point is to demonstrate
	the logic, not to have a user-friendly interface.'''

	def reveal_cells(self):
		print 'Enter no. of cells to reveal'
		n = raw_input('--->')
		numbered_cells = [i for i, v in enumerate([cell.public_value for cell in self.cells]) if v == '-']
		cell_indices = random.sample(numbered_cells, int(n))
		for ix in cell_indices:
			self.cells[ix].make_visible()
		self.display()

	def reveal_all(self):
		for cell in self.cells:
			cell.make_visible()
		self.display()

	def crude_interact(self):
		self.full_solve()
		self.display()
		self.reveal_cells()
		options_dict = {'1': self.reveal_cells,
						'2': self.reveal_all}

		while len([cell.public_value != cell.value for cell in self.cells]) != 0:
			print '''Choose an option:
	1) Reveal some cells.
	2) Reveal all.'''
			raw = raw_input('--->')
			func = options_dict[raw]
			func()

if __name__=="__main__":
	grid = SudokuGrid(3)
	grid.crude_interact()
