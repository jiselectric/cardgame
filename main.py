import numpy as np
class Card:
    def __init__(self, label, value):
        self.label = label
        self.value = value

class CardBatchMaker:
    def __init__(self, count=5):
        def int2char(x):
            chars = ('+', '-', '*', '/')
            if x < 13:
                return x
            else:
                return chars[x-13]

        self._labels = []
        while len(self._labels) < 16:
            t = np.random.randint(ord('A'), ord('Z')+1)
            if chr(t) not in self._labels:
                self._labels.append(chr(t))

        self._values = []
        while len(self._values) < 16:
            t = np.random.randint(1, 17)
            if int2char(t) not in self._values:
                self._values.append(int2char(t))
        
        self.cards = []
        self.batches = {}
        for label, value in zip(self._labels, self._values):
            self.batches[value] = label
            self.cards.append(Card(label, value))
        
        self.count = count
        
        
    
    def makeGame(self):
        target = 133
        solver = Solver(self.batches, target)
            
        while len(solver.answers) < self.count:
            target = np.random.randint(1, 20)
            solver = Solver(self.batches, target)
        return self.cards, target, solver.answers
            

class Host:
    def __init__(self, cards, target, answers):
        self.point = 0
        self.count = 0
        self.cards = cards
        self.target = target
        self.answerBook = {}
        for ans in answers:
            self.answerBook[ans] = True
    
    def getTables(self):
        self.tables = []
        for idx, card in enumerate(self.cards):
            if idx%4 == 0:
                self.tables.append([card])
            else:
                self.tables[idx//4].append(card)
            
    def showTables(self, showValues=''):
        for table in self.tables:
            for card in table:
                if card.label in showValues:
                    print(card.value, end="\t")
                else:
                    print(card.label, end="\t")
            print(end="\n")
    
    def showValues(self):
        for table in self.tables:
            for card in table:
                print(card.value, end="\t")
            print(end="\n")
    
    def isRight(self, ans):
        if ans in self.answerBook:
            if self.answerBook[ans]:
                self.answerBook[ans] = False
                return True
            else:
                return False
        else:
            return False
    
    def isOver(self):
        for ans in self.answerBook:
            if self.answerBook[ans]:
                return False
        return True
    
class Solver:
    def __init__(self, batches, target):
        self.answers = set()
        for i in range(1, 13):
            for j in range(1, 13):
                if i != j:
                    for op in ('+', '-', '*', '/'):
                        result = None
                        if op == '+':
                            result = i + j
                        elif op == '-':
                            result = i - j
                        elif op == '*':
                            result = i * j
                        else:
                            if i%j == 0:
                                result = i // j
                            else:
                                result = None
                        if result == target:
                            if op == '+' or op == '*':
                                m = i if i < j else j
                                n = j if i < j else i
                            else:
                                m = i
                                n = j
                            ans = batches[m]+batches[op]+batches[n]
                            self.answers.add(ans)
                        else:
                            continue
                else:
                    continue

