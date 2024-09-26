# several useful tools

import datetime
import calendar
from datetime import datetime


def readFile(name):
    file = open(name, "r")
    fileArray = file.readlines()
    file.close()
    return fileArray


def writeFile(new_Array, name):
    file = open(name, "w")
    file.writelines(new_Array)
    file.close()


def days(month):
    if month == 2:
        if calendar.isleap(datetime.datetime.now().year):
            return 29
        else:
            return 28
    elif month < 7:
        if month % 2 == 0:
            return 30
        else:
            return 31
    else:
        if month % 2 == 0:
            return 31
        else:
            return 30


def getMonthlyExp():
    file = readFile("settings.txt")
    fileread = file[5].strip()

    entries = fileread.split(", ")

    monthly = {key: float(value) for key, value in (entry.split(": ") for entry in entries)}

    return monthly


def savexp(newExpense):
    expenses = readFile("database.txt")
    expenses.append(str(newExpense.name)+', '+str(newExpense.amount)
                    +', '+str(newExpense.category)+', '+str(newExpense._date)+"\n")
    writeFile(expenses, "database.txt")
