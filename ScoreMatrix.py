def validSeq(seq):
        for i in seq:
            if i not in ['A', 'C', 'G', 'T']:
                raise ValueError(f"Invalid sequence. '{i}' is not a valid nucleotide.")

def makeStrLenThree(string):
    if len(string) > 3:
        raise ValueError("The string is longer than 3 characters.")
    
    result = ' ' * (3 - len(string)) + string

    return result


class ScoreCell:
    def __init__(self) -> None:
        self.cellValue = None

        self.valueComeFromUp = False
        self.valueComeFromLeft = False
        self.valueComeFromDiag = False

        self.validTraces = [False, False, False]

    def __repr__(self) -> str:
        return f'{self.cellValue}'
    
    def setCellValue(self, value):
        self.cellValue = value

    def getCellValue(self):
        return self.cellValue
    
    def setValueComeFromUp(self):
        self.valueComeFromUp = True

    def setValueComeFromLeft(self):
        self.valueComeFromLeft = True

    def setValueComeFromDiag(self):
        self.valueComeFromDiag = True

    def haveValueComeFromUp(self) -> bool:
        return self.valueComeFromUp
    
    def haveValueComeFromLeft(self) -> bool:
        return self.valueComeFromLeft
    
    def haveValueComeFromDiag(self) -> bool:
        return self.valueComeFromDiag


class ScoreMatrix:
    def __init__(self, matchScore, missScore, gapScore, vSeq: str, hSeq: str):
        self.matchScore = matchScore
        self.missScore = missScore
        self.gapScore = gapScore

        self.biggestAlignments = []

        self.vSeq = vSeq.upper() # Make sure the sequences are in uppercase
        self.hSeq = hSeq.upper()

        validSeq(self.vSeq) # Check if the sequences only contain 'A', 'C', 'G' or 'T'
        validSeq(self.hSeq)

        self.vSeq = 'U' + self.vSeq # Add a 'U' to the beginning of the sequences
        self.hSeq = 'U' + self.hSeq

        self.matrix = [[ScoreCell() for i in range(len(self.hSeq))] for j in range(len(self.vSeq))] # Initialize the matrix

        self.findScores() # Fill the matrix with the scores

    def findScores(self): # Find and fill the matrix with the scores
        self.matrix[0][0].setCellValue(0) # Set the first cell to 0

        for i in range(1, len(self.matrix[0])): # Set the first row and column to the gap score
            previousValue = self.matrix[0][i - 1].getCellValue()
            
            self.matrix[0][i].setCellValue(self.gapScore + previousValue)
            self.matrix[0][i].setValueComeFromLeft()

        for i in range(1, len(self.matrix)):
            previousValue = self.matrix[i - 1][0].getCellValue()

            self.matrix[i][0].setCellValue(self.gapScore + previousValue)
            self.matrix[i][0].setValueComeFromUp()

        for i in range(1, len(self.vSeq)): # Fill the rest of the table
            for j in range(1, len(self.hSeq)):
                upValue = self.matrix[i - 1][j].getCellValue() + self.gapScore
                leftValue = self.matrix[i][j - 1].getCellValue() + self.gapScore

                if self.vSeq[i] == self.hSeq[j]:
                    diagValue = self.matrix[i - 1][j - 1].getCellValue() + self.matchScore
                else:
                    diagValue = self.matrix[i - 1][j - 1].getCellValue() + self.missScore

                self.matrix[i][j].setCellValue(max(upValue, leftValue, diagValue))

                if upValue == self.matrix[i][j].getCellValue():
                    self.matrix[i][j].setValueComeFromUp()
                
                if leftValue == self.matrix[i][j].getCellValue():
                    self.matrix[i][j].setValueComeFromLeft()
                
                if diagValue == self.matrix[i][j].getCellValue():
                    self.matrix[i][j].setValueComeFromDiag()

    def printMatrix(self):
        for i in range(len(self.matrix)-1, -1, -1):
            print('\033[36m' + f' {self.vSeq[i]} ' + '\033[0m' + '\033[32m' + ''.join([f' {makeStrLenThree(str(j))} ' for j in self.matrix[i]]) + '\033[0m')

        print('\033[36m' + '   ' + ''.join([f'  {i}  ' for i in self.hSeq]) + '\033[0m')

    def getBiggestAlignments(self):
        return self.findAlignmentAt(len(self.vSeq) - 1, len(self.hSeq) - 1)
        
    def findAlignmentAt(self, i, j):
        listOfAlignments = []

        def backTrace(i: int, j: int, vAlign = "", hAlign = ""):
            nonlocal listOfAlignments
            nonlocal self
            
            if (i == 0) and (j == 0):
                alignment = f'{vAlign}\n{hAlign}\n\n'

                listOfAlignments.append(alignment)

            else:
                if self.matrix[i][j].haveValueComeFromUp():
                    tempV = self.vSeq[i] + vAlign
                    tempH = '-' + hAlign

                    backTrace(i - 1, j, tempV, tempH)

                if self.matrix[i][j].haveValueComeFromLeft():
                    tempV = '-' + vAlign
                    tempH = self.hSeq[j] + hAlign

                    backTrace(i, j - 1, tempV, tempH)

                if self.matrix[i][j].haveValueComeFromDiag():
                    tempV = self.vSeq[i] + vAlign
                    tempH = self.hSeq[j] + hAlign

                    backTrace(i - 1, j - 1, tempV, tempH)

        backTrace(i, j)

        return listOfAlignments
