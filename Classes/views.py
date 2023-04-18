# start views.py
import os
import shelve
import lofigui
import envelope # todo: dit zou niet moeten
import controller

def startView():
    """
    What user sees when running the program.
    """
    gui = lofigui.LofiGUI("ENVELOPE BUDGETTING")
    gui.frame("Hi there!","Welcome to the wild world of envelope budgetting!")
    gui.listPrompt("Please choose:", [["Open budget", openView],
                                      ["Create budget", lambda: print("todo create")], 
                                        ["Delete budget", deleteView]])

def openView():
    """
    Show a list with existing budgets. If none, propose to create one.
    """
    gui = lofigui.LofiGUI("OPEN BUDGET")
    budgets = controller.getBudgets()
    if budgets != False and len(budgets) > 0:
        gui.frame("Budgets found.")
        choiceList= []
        for budget in budgets:
            # the following is necessary to assign parameter (https://stackoverflow.com/questions/3431676/creating-functions-or-lambdas-in-a-loop-or-comprehension)
            def printBudget(budget=budget):
                showView(controller.openBudget(budget))
            choiceList.append([budget, printBudget])
        gui.listPrompt("Choose a budget to open:", choiceList)
    else:
        gui.yesNo("No existing budgets found. Create a new budget?", lambda: setupView())

def deleteView():
    """
    Pick a budget to delete
    """
    # TODO refactor together with openView
    gui = lofigui.LofiGUI("DELETE BUDGET")
    budgets = controller.getBudgets()
    if budgets != False and len(budgets) > 0:
        gui.frame("Budgets found.")
        choiceList = []
        for budget in budgets:
            def deleteBudget(budget=budget):
                controller.deleteBudget(budget)
            choiceList.append([budget, deleteBudget])
        gui.listPrompt("Choose a budget to delete:", choiceList)
        gui.yesNo("Delete another budget?", deleteView)
    else:
        # todo create decent create budget function
        gui.frame("No budgets found.")
        gui.yesNo("Create a new budget?", lambda: setupview())

def createView():
    pass

def editView(budget):
    """
    Add, change or delete envelopes, targets and sums in your budget.
    """
    showView(budget)
    # edit posibilities: add/delete envelope, fill envelope, spend money, add/delete categorie
    pass

def setupView():
    """
    If no budget, propose to create new budget, 
    fill it with some first categories and envelopes and then save it.
    """
    prompt = input("Create new budget. Type 'exit' to quit. Your budget's name: ") # check if not empty and such!!
    if prompt == "exit":
        print("Ok, bye!")
        return
    # naar controller verhuizen!
    budget = envelope.Budget(prompt)
    gui = lofigui.LofiGUI(budget.name)
    gui.frame("Budget '%s' successfully created." % budget.name)
    while True:
        catPrompt = input("\nNow add some categories. Type 'done' to quit: ")
        if catPrompt == "done": break
        newCategory = envelope.Category(catPrompt)
        budget.addCategory(newCategory)
        while True:
            print("Before adding another category, let's add some envelopes to '%s'." % newCategory.name)
            print("If you are finished inputting, then type 'done'.")
            envPrompt = input("How would you like to name this envelope? ")
            if envPrompt == 'done':
                print("Done creating envelopes for category '%s'.\n" % newCategory.name)
                break
            occurPrompt = input("How many times a year do you need to fill this envelope? Enter 1, 12 or 4: ")
            targetPrompt = input("Whith what amount should it be filled every time? ")
            if occurPrompt == "1":
                newEnvelope = envelope.Yearly(envPrompt, float(targetPrompt))
            elif occurPrompt == "12":
                newEnvelope = envelope.Monthly(envPrompt, float(targetPrompt))
            elif occurPrompt == "4":
                newEnvelope = envelope.Quarterly(envPrompt, float(targetPrompt))
            else:
                print("You entered the wrong number. Please start over.\n")
                break
            newCategory.addEnvelope(newEnvelope)
            print("Envelope %s successfully created.\n" % newEnvelope.name)
    gui.frame("Great! You have succesfully created and filled your budget.")
    showView(budget)
    firstSaveView(budget)

def showView(budget):
    """
    Print a nice overview of the budget
    """
    gui = lofigui.LofiGUI(budget.name)
    gui.start()
    gui.write("For this budget you need %s a month" % budget.getTotalBudgetTarget())
    gui.title("Categories")
    for category in budget.categories:
        gui.title(category.name)
        gui.write("For this category you need %s a month." % category.getTotalTargets())
        gui.write("=> Envelopes:")
        for env in category.envelopes:
            gui.write("For this envelope you need %s every %s days" % (env.target, env.period))
            gui.write(env.name + ": " + str(env.target))
    gui.write()
    gui.stop()

def firstSaveView(budget):
    while True:
        savePrompt = input("\nSave this budget? Y or N: ")
        if savePrompt == "Y":
            budgetName = budget.name + ".budget"
            print("Saving your budget %s ..." % budgetName)
            db = shelve.open(budgetName) # check if exists? to avoid overwrite
            db[budget.name] = budget
            db.close()
            print("Your budget has been saved. Happy Budgetting!")
            break
        if savePrompt == "N":
            print("Giving it another try? Good idea!")
            break
        else:
            print("You have to enter Y or N.")


# TODO tests