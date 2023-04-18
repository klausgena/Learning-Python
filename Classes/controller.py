# File controller.py programming logic between model and views
import os
import shelve
import envelope

# todo: write createbudget, rewrite openbudget?

def getBudgets():
    """
    Check for existing budgets in script dir 
    and return list of budgets.
    """
    budgets = []
    for file in os.listdir("."):
        if file.endswith(".budget.dir"):
           cleanName = file.rsplit(".", 1)[0]
           budgets.append(cleanName)
    if budgets == []:
        return False
    else:
        return budgets

def openBudget(budgetFileName):
    """
    Opens a budget file and returns
    a budget object
    """
    if budgetExists(budgetFileName):
        budgetName = budgetFileName.rsplit(".", 1)[0]
        db = shelve.open(budgetFileName)
        return db[budgetName]
    else:
        return False

def createBudget(budgetFileName):
    """
    Create a budget starting from a file name
    and save it.
    """
    if budgetExists(budgetFileName):
        return False
    else:
        shortName = budgetFileName.rsplit(".", 1)[0]
        newBudget = envelope.Budget(shortName)
        db = shelve.open(budgetFileName)
        db[newBudget.name] = newBudget
        db.close()
        return True

def deleteBudget(budgetFileName):
    """
    Deletes a budget file out of a folder
    """
    if budgetExists(budgetFileName):
        budgetFileNames = [budgetFileName + ".bak", 
                       budgetFileName + ".dat",
                       budgetFileName + ".dir"]
        for file in budgetFileNames:
            if file in os.listdir("."):
                os.remove(file)
        return True
    else:
        return False
    

def budgetExists(budgetFileName):
    """
    Return True if budget file exists, 
    otherwise False.
    """
    budgetFileNames = [budgetFileName + ".bak", 
                       budgetFileName + ".dat",
                       budgetFileName + ".dir"]
    if budgetFileNames[0] in os.listdir("."):
        return True
    return False



# TESTS

if __name__ == "__main__":
    
    print(createBudget("This sucks.budget"))
    print(getBudgets())
    print(openBudget("test.budget"))
    print(openBudget("This sucks.budget"))
    print(deleteBudget("This sucks.budget"))
    print(getBudgets())