from RowColumn import RowColumn


class Cell:
    letter = None
    number = None
    box = None
    row = None
    column = None
    validValues = None
    rowColumnLength = None

    def __init__(self, letter, number, box, rowColumnLength):
        self.letter = letter
        self.number = number
        self.box = box
        self.rowColumnLength = rowColumnLength

    def assignValue(self, value):
        if self.isValueValid(value):
            self.number = value
            self.row.addValue(value)
            self.column.addValue(value)
            return True
        return False

    # def bestAssignValue(self, value):
    #     if self.bestIsValueValid(value):
    #         self.number = value
    #         self.row.addValue(value)
    #         self.column.addValue(value)
    #         return True
    #     return False

    # def bestRemoveValue(self, value):
    #     self.number = 0
    #     self.row.removeValue(value)
    #     self.column.removeValue(value)

    def removeValue(self, value):
        self.number = 0
        self.row.removeValue(value)
        self.column.removeValue(value)

    def isValueValid(self, value):
        return self.row.isValueValid(value) and self.column.isValueValid(value) and self.box.isValueValid(value)
