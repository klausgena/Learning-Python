# File person.py (start)
"""
Record and process information about people. 
Run this file directly to test its classes.
"""
from classtools import AttrDisplay                          # use generic display tool

class Person(AttrDisplay):                                  # add custom __repr__ at this level
    """
    Create and process person records
    """
    def __init__(self, name, job=None , pay=0):
        self.name = name
        self.job = job
        self.pay = pay
    # Encapsulation: methods in class
    def lastName(self):
        return self.name.split()[-1]                        # Assumes last name is last word
    def giveRaise(self, percent):
        self.pay = int(self.pay * (1 + percent))            # percent must be 0.x

class Manager(Person):
    """
    A customized person with special requirements
    """
    def __init__(self, name, pay):
        Person.__init__(self, name,'Manager', pay)          # job name is implied
    def giveRaise(self, percent, bonus=.1):
        Person.giveRaise(self, percent + bonus)

if __name__ == '__main__':
    bob = Person('Bob Smith')
    sue = Person('Sue Jones', job='Dev', pay=100000)
    dave = Manager('Dave Purdue', pay=250000)
    print(bob)
    print(sue)
    print(dave)
    print(sue.lastName(), bob.lastName())
    sue.giveRaise(.1)
    dave.giveRaise(.1)
    print(sue)
    print(dave)
    print(dave.lastName())