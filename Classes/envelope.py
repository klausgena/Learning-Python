# start file envelope.py

# TODO: add envelope with target date, even more than a year

"""
Envelope budgetting tool.
"""
from classtools import AttrDisplay
from datetime import date

TODAY = date.today().timetuple().tm_yday

class Budget(AttrDisplay):
    """
    Main class, containing the categories, creating a budget.
    Calculate the totals for a budget, etc.
    """
    def __init__(self, name="Unnamed", *args):
        """Enter name as string, followed by categories"""
        self.name = name
        self.categories = list(args)
    def addCategory(self, category):
        self.categories.append(category)
    def showAllCategories(self):
        for category in self.categories:
            print(category.name)
            category.showAllEnvelopes()
    def getTotalBudgetTarget(self):
        """Get the total monthly budget target"""
        budgetTotal = 0
        for category in self.categories:
            budgetTotal = budgetTotal + category.getTotalTargets()
        return budgetTotal
    def getTotalFilled(self):
        fillTotal = 0
        for category in self.categories:
            fillTotal = fillTotal + category.getTotalFilled()
        return fillTotal


class Category(AttrDisplay):
    """
    A category contains envelopes for broader expense posts,
    like Car for example (with envelopes as Fuel, Parking, etc.)
    """
    def __init__(self, name="Unnamed", *args):
        """Enter name as string, followed by categories"""
        self.name = name
        self.envelopes = list(args)
    def addEnvelope(self, envelope):
        self.envelopes.append(envelope)
    def showAllEnvelopes(self):
        for envelope in self.envelopes:
            print(envelope)
    def getTotalTargets(self):
        """Gives the monthly target amount for this category"""
        targetTotal = 0
        for envelope in self.envelopes:
            adjustedTarget = envelope.target / (12 / envelope.occurrence)   # Category can contain envelopes with different frequencies/occurrences
            targetTotal = targetTotal + adjustedTarget
        return round(targetTotal, 2)
    def getTotalFilled(self):
        fillTotal = 0
        for envelope in self.envelopes:
            fillTotal = fillTotal + envelope.sum
        return fillTotal

class Envelope(AttrDisplay):
    """
    Master class to create and process budget envelopes
    This is default (yearly) envelope
    """
    def __init__(self, name, target, sum, occurrence):
        self.name = name
        self.target = target
        self.sum = sum
        self.occurrence = occurrence
        self.today =  TODAY
        self.period = round((365/self.occurrence), 2)               # too shabby. Use timedelta? Or modulo?
    def addMoney(self, sum):
        self.sum = self.sum + sum
    def spendMoney(self, sum):
        self.sum = self.sum - sum
    def percentFilled(self):                                        # Warn when overfilled!
        """Envelope filled for # percent"""
        if self.sum == 0:
            return 0.00
        return round(( 100 * 1 / (self.target / self.sum)), 2)
    def daysLeftToFill(self):
        """Days left to fill envelope"""
        return int(self.period - (self.today % self.period))
    def todaysTarget(self):
        return (self.today % self.period) * (self.target / self.period)
    def amountOffTrack(self):
        return round((self.sum - self.todaysTarget()), 2)
    def percentOffTrack(self):
        return round((100 * (self.amountOffTrack() / self.todaysTarget())), 2)

class Monthly(Envelope):
    """
    Monthly filled envelope
    """
    def __init__(self, name, target=0, sum=0):
        Envelope.__init__(self, name, target, sum, 12)

class Quarterly(Envelope):
    """
    Quarterly filled envelope
    """
    def __init__(self, name, target=0, sum=0):
        Envelope.__init__(self, name, target, sum, 4)

class Yearly(Envelope):
    """
    Yearly filled envelope (one time expense, 
    might occur any time in the year)
    """
    def __init__(self, name, target=0, sum=0):
        Envelope.__init__(self, name, target, sum, 1)


# TESTS

if __name__ == '__main__':
   
    hond = Yearly('Hond', target = 250, sum = 48.63)
    eten = Monthly('Eten', 600, 201)
    belastingen = Quarterly('Belastingen', 1500, 1170)
    envelopes = [hond, eten, belastingen]

    hond.addMoney(100)
    print(hond)

    belastingen.spendMoney(170)
    print(belastingen)

    print("===")

    for envelope in envelopes:
        print(envelope)
        print(envelope.daysLeftToFill())
        print(envelope.percentFilled())
        print(envelope.percentOffTrack())
        print(envelope.amountOffTrack())
        print("===")

    print("Categories")

    household = Category("Huishouden", hond, eten)
    taxes = Category("Belastingen", belastingen)
    car = Category("Auto")

    car.addEnvelope(Monthly('fuel', 100, 20))

    print(household)

    print(household.getTotalTargets())
    print(household.getTotalFilled())
    print(taxes.getTotalFilled())

    # add envelope

    socialTaxes = Quarterly('sociale lasten', 1500, 300)
    taxes.addEnvelope(socialTaxes)
    taxes.showAllEnvelopes()

    # Budget
    print("=== BUDGET ===")

    myBudget = Budget("My Budget", household, taxes, car)
    print(myBudget.getTotalBudgetTarget())
    print(myBudget.getTotalFilled())

    myBudget.showAllCategories()
