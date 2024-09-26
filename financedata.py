# This Class will handle all finance Data without longterm data storage

import filehandle as file
from datetime import date
from datetime import datetime
from expense import Expense

class FinanceData:
    def __init__(self, fileName):
        self._fileName = fileName
        self._file = file.readFile(self._fileName)
        self.date = [int(x) for x in self._file[1][:-1].split("-")]
        # 0: year, 1: month, 2: day, 3: weekday (mon = 0, sun = 6)

        # total
        if datetime.now().month > self.date[1] or datetime.now().year > self.date[0]:
            datasave = file.readFile("surplusdata.txt")
            datasave.append(self._file[1])
            datasave.append(self._file[3])
            file.writeFile(datasave, "surplusdata.txt")

            monthlyExpenses = file.getMonthlyExp()
            self.total = float(file.readFile("settings.txt")[3])

            for x in monthlyExpenses.values():
                self.total -= x
            self._file[3] = str(self.total) + '\n'
            file.writeFile(self._file, self._fileName)

        else:
            self.total = float(self._file[3][:-1])

        # weekly
        if self.date[3] > datetime.today().weekday():
            self.weekly = self.total / (file.days(self.date[1])/7)
            self._file[5] = str(self.weekly) + '\n'
            file.writeFile(self._file, self._fileName)
        else:
            self.weekly = float(self._file[5][:-1])

        # daily
        if datetime.now().day > self.date[2]:
            self.daily = self.total / file.days(self.date[1])
            self._file[7] = str(self.daily) + '\n'
            file.writeFile(self._file, self._fileName)
        else:
            self.daily = float(self._file[7][:-1])
        # date update
        self._file[1] = str(date.today())+'-'+str(datetime.today().weekday()) + "\n"
        file.writeFile(self._file, self._fileName)

    def load(self):
        '''to re-load total, daily and weekly'''

        # total
        monthlyExpenses = file.getMonthlyExp()
        self.total = float(file.readFile("settings.txt")[3])

        for x in monthlyExpenses.values():
            self.total -= x
        self._file[3] = str(self.total) + '\n'

        # weekly
        self.weekly = self.total / (file.days(self.date[1]) / 7)
        self._file[5] = str(self.weekly) + '\n'

        # daily
        self.daily = self.total / file.days(self.date[1])
        self._file[7] = str(self.daily) + '\n'
        file.writeFile(self._file, self._fileName)
        return self

    def __sub__(self, other):
        if not isinstance(other, Expense):
            raise TypeError(f"Subtraction only allowed with 'Expense' instance, not {type(other).__name__}")
        self.total -= other.amount
        self.daily -= other.amount
        self.weekly -= other.amount
        self._file[3] = str(self.total) + '\n'
        self._file[5] = str(self.weekly) + '\n'
        self._file[7] = str(self.daily) + '\n'
        file.writeFile(self._file, self._fileName)
        return self

fd = FinanceData("finance data/standard.txt")
