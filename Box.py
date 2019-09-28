class Box:
    result = None
    operation = None
    cells = None
    options = None

    def __init__(self, result, operation):
        self.result = result
        self.operation = operation
        self.cells = []
        self.options = []

    def isValueValid(self, value):
        emptyCount = 0
        values = []
        for cell in self.cells:
            if cell.number == 0:
                emptyCount += 1
            else: #todo is this right?
                values.append(cell.number)
        values.append(value)
        if emptyCount > 1:
            return True

        if self.operation == "*":
            starting = 1
            for value in values:
                starting = starting * value
            return starting == int(self.result)
        elif self.operation == "/":
            divisionCheckOne = values[0] / values[1] == int(self.result)
            remainderCheckOne = values[0] % values[1] == 0
            divisionCheckTwo = values[1] / values[0] == int(self.result)
            remainderCheckTwo = values[1] % values[0] == 0
            return (divisionCheckOne and remainderCheckOne) or (divisionCheckTwo and remainderCheckTwo)
        elif self.operation == "+":
            starting = 0
            for value in values:
                starting = starting + value
                truth = starting == int(self.result)
            return truth
        elif self.operation == "-":
            return (values[0] - values[1] == int(self.result)) or (values[1] - values[0] == int(self.result))
        else:
            return False

    def calculateOptions(self, solutions, index):
        rowLength = self.cells[0].rowColumnLength
        cellCount = len(self.cells)

        # Base case: success
        total = 0
        if self.operation == "*":
            total = 1
            for s in solutions:
                total = total * s
        elif self.operation == "+":
            total = 0
            for s in solutions:
                total = total + s
        if total == int(self.result):
            copy = []
            for s in solutions:
                copy.append(s)
            if copy not in self.options:
                self.options.append(copy)

        if index >= cellCount:
            return False

        for i in range(rowLength):
            i = i + 1
            solutions[index] = i
            if self.calculateOptions(solutions, index + 1):
                return True
        return False

    def generateCellsValidValues(self):
        uniqueNumbers = set([])
        for i in range(len(self.options)):
            for j in range(len(self.options[i])):
                uniqueNumbers.add(self.options[i][j])
        for cell in self.cells:
            cell.validValues = uniqueNumbers

    # TODO do we need to store options for the box anymore, or can we just use this function to get the values for the cells?
    def getOptions(self):
        if len(self.options) > 0:
            return self.options
        self.options = []
        rowLength = self.cells[0].rowColumnLength
        cellCount = len(self.cells)
        if self.operation == "*" or self.operation == "+":
            solutions = []
            for i in range(cellCount):
                solutions.append(0)
            self.calculateOptions(solutions, 0)
            self.generateCellsValidValues()
            return self.options
        elif self.operation == "-":
            for i in range(rowLength):
                i = i + 1
                other = i - int(self.result)
                if (0 < other < rowLength + 1) and (other != i):
                    self.options.append([i, other])
                    self.options.append([other, i])
                self.generateCellsValidValues()
            return self.options
        elif self.operation == "/":
            for i in range(rowLength):
                i = i + 1
                other = i / int(self.result)
                remainder = i % int(self.result)
                if remainder == 0 and other != i:
                    self.options.append([i, other])
                    self.options.append([other, i])
                    # todo handle duplicates like [1,1]
            self.generateCellsValidValues()
            return self.options

    # def applyValues(self, values):
    #     for i in range(len(values)):
    #         if not self.cells[i].bestAssignValue(values[i]):
    #             for cell in self.cells:
    #                 cell.bestRemoveValue(cell.number)
    #             return False
    #     return True
