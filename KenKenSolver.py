from Box import Box
from Cell import Cell
from RowColumn import RowColumn
import math
import random
import time

# TODO Does this need to be able to accept multiple inputs one after another?

class KenKenSolver:
    rowLength = int(raw_input())
    rows = []
    columns = []
    boxes = {}
    cells = []
    backtrackIterations = 0
    bestBacktrackingIterations = 0

    # Create rows and columns
    for x in range(rowLength):
        row = RowColumn(x)
        column = RowColumn(x)
        rows.append(row)
        columns.append(column)

    def get_input(self):
        # Get each line of letters
        for x in range(self.rowLength):
            letters = raw_input()
            # Use each letter in the line to create a cell.  Create the cell list.
            for letter in letters:
                self.boxes[letter] = "test"
                cell = Cell(letter, 0, None, self.rowLength)
                self.cells.append(cell)
        # Get Letter to Result/Operation mappings.  Create boxes.
        for x in range(len(self.boxes)):
            lineSections = raw_input().split(':')
            character = lineSections[0]
            numberAndOperation = lineSections[1]
            operation = numberAndOperation[len(numberAndOperation) - 1]
            number = numberAndOperation[:-1]
            box = Box(number, operation)
            self.boxes[character] = box
        # Assign boxes to cells
        for cell in self.cells:
            box = self.boxes[cell.letter]
            cell.box = box
            box.cells.append(cell)
        # Assign rows and columns to cells
        for cellIndex in range(len(self.cells)):
            self.cells[cellIndex].row = self.rows[cellIndex / self.rowLength]
            self.cells[cellIndex].column = self.columns[cellIndex % self.rowLength]

    def print_puzzle(self):
        line = ""
        for i in range(len(self.cells)):
            if (i % math.sqrt(len(self.cells)) == 0) and (i != 0):
                print(line)
                line = ""
            line += str(self.cells[i].number) + " "
        print(line)
        print("")

    def clearPuzzle(self):
        for cell in self.cells:
            cell.removeValue(cell.number)
        self.backtrackIterations = 0

    # TODO Ensure handling of iteration count is correct
    # For every cell, tries every number from 1 to the number of cells in a row.
    # If none are valid for a cell,
    # retreat to the previous cell and change its value to the next highest value that is valid for that cell.
    # Then continue to the next cell, trying all values from there.
    def backtrack(self, index):
        self.backtrackIterations += 1
        # Base case: reached the end
        if index == len(self.cells):
            self.print_puzzle()
            print(self.backtrackIterations)
            self.clearPuzzle()
            return True
        # From 1 to the number of cells in a row,
        for i in range(self.rowLength):
            i = i + 1
            # If this value for this cell is valid,
            if self.cells[index].assignValue(i):
                # Assign it and try the next.
                if self.backtrack(index + 1):
                    return True
                else:
                    # Empty the cell
                    self.cells[index].removeValue(i)
        return False

    sortedCells = []

    # Sort the cells in ascending order according to how many valid values that cell has.
    # For example: if the row length is 6, and a box has 2 cells, and they must add up to 11,
    # then each cell could only contain 6 or 5, because those are the only 2 values from 1 to 6 that add up to 11.
    # Each of these cells would have 2 valid values, and would likely be near the beginning of this list.
    # This list is stored in self.sortedCells
    def sortCells(self):
        for i in range(len(self.sortedCells)):
            value = len(self.sortedCells[i].validValues)
            if i < len(self.sortedCells) - 1:
                nextValue = len(self.sortedCells[i+1].validValues)
                # If the current cell has more options than the next cell,
                if value > nextValue:
                    # Switch the cells.
                    temp = self.sortedCells[i+1]
                    self.sortedCells[i+1] = self.sortedCells[i]
                    self.sortedCells[i] = temp
                    self.sortCells() #todo probably inefficient

    # Entry point for the best backtracking solution.
    def bestBacktracking(self, index):
        # Generate the valid options for each box.  This function also generates each cell's validValues list.
        for key in self.boxes:
            self.boxes[key].getOptions()
        start_time = time.time()
        # Add cells to sortedCells.
        for cell in self.cells:
            self.sortedCells.append(cell)
        # Sort the cells.
        self.sortCells()
        # Use sortedCells to conduct the best backtracking search.
        self.bestBacktrackingSearch(self.sortedCells, index)
        # print("--- %s seconds ---" % (time.time() - start_time))

    # The recursive search that the best backtracking function uses.
    def bestBacktrackingSearch(self, sortedCells, index):
        self.bestBacktrackingIterations += 1
        # Base case: the search has passed the last cell
        if index == len(sortedCells):
            # self.print_puzzle()
            print(self.bestBacktrackingIterations)
            return True
        cell = sortedCells[index]
        options = cell.validValues
        # For every possible valid value for the cell,
        for i in options:
            # If that value is valid according to the current row and column situation,
            if cell.assignValue(i):
                # Assign it and search the next cell
                if self.bestBacktrackingSearch(sortedCells, index + 1):
                    return True
                else:
                    # Empty the cell
                    cell.removeValue(i)
        return False

    def localSearch(self):
        # number of random restarts allowed: length of loop
        bestSoFar = 36
        # make set of states that have been seen
        statesSet = set()

        for i in range(1000):
            degrees = 400
            self.assignRandomValues()
            #print('current puzzle')
            #self.print_puzzle()
            #print(' ')
            # evaluate current state
            currEn = self.getConstraintsViolated()
            if currEn == 0:
                self.print_puzzle()
                return 'solution found'
            # store old value and which cell in case of rejection
            # change 1 cell value (neighbor node of slightly different state);
            # check: is this different from old value?
            improving = True
            iterations = 0
            numWorse = 0

            while improving:
                iterations += 1
                if iterations % 4 == 0:
                    degrees = degrees * 0.8
                    #print('degrees')
                    #print(degrees)
                    #print(' ')
                valDiff = False
                cellToPull = random.randint(1, (len(self.columns) ** 2)-1)
                currValCell = self.cells[cellToPull].number
                while not valDiff:
                    self.cells[cellToPull].number = random.randint(1, len(self.columns))
                    if currValCell != self.cells[cellToPull].number:
                        valDiff = True
                # evaluate new state
                # print(iterations)
                # get energy (constraints violated) of neighbor state
                nextEn = self.getConstraintsViolated()
                #print('next puzzle')
                #self.print_puzzle()
                #print('constraints violated: ')
                #print(nextEn)
                #print (' ')
                # if neighbor state is better, accept. otherwise, accept based on probability
                if nextEn < currEn:
                    #print('next is better')
                    currEn = nextEn
                    numWorse = 0
                else:
                    numWorse += 1
                    if self.getProbabilityAccept(degrees, nextEn) > random.random:
                        currEn = nextEn
                        #print('next is worse, accept anyway with prob:')
                        #print (self.getProbabilityAccept(degrees, nextEn))
                        #print (' ')
                    else:
                        # restore puzzle to former state- neighbor not accepted
                        self.cells[1].number = currValCell
                # if not improving after x iterations, random restart but store current best solution
                if numWorse > 100:
                    if bestSoFar > currEn:
                        bestSoFar = currEn
                    #print ('not improving. random restart now')
                    improving = False
            # if solution not found after x restarts, quit
        print('no solution found')
        print ('best so far:')
        print(bestSoFar)
        return False

    def assignRandomValues(self):
        valuesAvailable = [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6]

        for i in range(len(self.cells)):
            self.cells[i].number = random.choice(valuesAvailable)
            valuesAvailable.remove(self.cells[i].number)
        # print('len of columns:')
        # print(len(self.columns))
        return

    def decreaseTemp(self, temp):
        temp = temp * 0.8

    def getProbabilityAccept(self, temp, energy):
        return 1 - (energy / temp)

    def getConstraintsViolated(self):
        invalid = 0
        for cell in self.cells:
            if not (cell.isValueValid(cell.number)):
                invalid += 1
        return invalid

    def stateToString(self):
        stateString = ''
        for cell in self.cells:
            stateString = stateString + str(cell.number)
        return stateString
