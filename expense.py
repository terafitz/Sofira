from datetime import datetime


class Expense:
    def __init__(self, name, amount, category, date):
        self.name = name
        self.amount = amount
        self.category = category
        if not hasattr(self, '_date'):
            if date == "yyyy/mm/dd/hh/mm":
                date = datetime.now()
                date_formatted = date.strftime("%Y/%m/%d/%H/%M")
                self._date = date_formatted
            else:
                self._date = date

    def younger(self, other):
        '''Checks if dates are equal/lower'''
        check = True
        selfdateArray = self._date.split("/")
        otherdateArray = other._date.split("/")
        for x,y in zip(selfdateArray, otherdateArray):
            if x > y:
                check = False
        return check

    def older(self, other):
        '''Checks if dates are equal/higher'''
        check = True
        selfdateArray = self._date.split("/")
        otherdateArray = other._date.split("/")
        for x,y in zip(selfdateArray, otherdateArray):
            if x < y:
                check = False
        return check

    def lower(self, other):
        if self.amount < other._amount: return True
        else:
            return False

    def higher(self, other):
        if self.amount > other._amount: return True
        else:
            return False
