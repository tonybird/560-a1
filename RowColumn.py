class RowColumn:
    usedValues = None
    idNumber = None

    def __init__(self, idNumber):
        self.usedValues = set()
        self.idNumber = idNumber

    def isValueValid(self, value):
        return value not in self.usedValues

    def addValue(self, value):
        self.usedValues.add(value)

    def removeValue(self, value):
        if value in self.usedValues:
            self.usedValues.remove(value)