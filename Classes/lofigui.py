# start file lofigui.py
"""
Low Quality less eyesore CLI GUI
"""

class LofiGUI:
    """
    Class that initiates a GUI window in CLI,
    with elements as rulers, boxes, titles, tables, etc.
    """
    def __init__(self, name="NoName", width=80):
        self.name = name
        self.width = width
    def calculateMargins(self, string):
        leftMargin = int((self.width /2) - (len(string) / 2)) - 1
        rightMargin = self.width - (leftMargin + len(string)) - 2
        return {"left" : leftMargin, "right" : rightMargin}
    def start(self):
        leftPart = int((self.width / 2) - (len(self.name) / 2)) - 1
        rightPart = self.width - (leftPart + len(self.name)) - 2
        reset = "\033[2J"
        ruler = reset + "\n+" + leftPart * "-" + self.name.upper() + rightPart * "-" + "+"
        print(ruler)    # Initialize GUI Frame
    def stop(self):
        print("+" + (self.width - 2) * "-" + "+\n")
    def title(self, title):
        margins = self.calculateMargins(title)
        self.write()
        print("+" + " " * margins["left"] + title.upper() + margins["right"] * " " + "+")
        print("+" + " " * margins["left"] + len(title) * "=" + margins["right"] * " " + "+")
        self.write()
    def write(self, string=""):        # Does not work when multiline?
        formattedString = "+ " + string + (self.width - len(string) - 3) * " " + "+"
        print(formattedString)
    def frame(self, *strings):
        """Make frame, followed by random list of strings"""
        self.start()
        self.write()
        for string in strings:
            self.write(string)
        self.write()
        self.stop()
    def yesNo(self, prompt, yes, no="break"):
        """
        Yes/No prompt with lambda functions
        """
        while True:
            answer = input(prompt + " Type Y or N: ")
            if answer in ["Y", "y", "yes", "Yes", "YES"]:
                yes()
                break
            elif answer in ["N", "n", "no", "NO"]:
                if no== "break":
                    break
                else:
                    no()
                    break
            else:
                print("Enter Y or N.")
    def listPrompt(self, question: str, choices):
        """
        Prompt with choice list (a list with nested list: name: function)
        """
        choiceList = ""
        for count, choice in enumerate(choices):
            choiceList = choiceList + self.colors("magenta", str(count)) + ") " + choice[0] + "\n"
        question = question + "\n" + choiceList
        while True:
            answer= input("[?] " + question)
            print("\u001b[1A\u001b[1K") # clear line
            # TODO check if input is int
            # THE FOR LOOP IS WRONG??? IT DOES EVERYTHING ALWAYS??
            for i in range(len(choices)):
                if int(answer) == i:
                    choices[int(answer)][1]()
                    return
            print("Pick a number.")
    # colors
    def colors(self, color, str):
        """Color the text"""
        colors ={"red": "\u001b[31m",
                 "black": "\u001b[30m",
                 "green": "\u001b[32m",
                 "yellow": "\u001b[33m",
                 "blue": "\u001b[34m",
                 "magenta": "\u001b[35m",
                 "cyan": "\u001b[36m",
                 "white": "\u001b[37m"}
        if color in colors:
            return colors[color] + str + "\u001b[0m"
        else:
            print("This color is not in the list. Pick an existing color.")


# TESTS

if __name__ == '__main__':
    
    gui = LofiGUI("Mijn kleine budgetje", 80)
    gui.start()
    gui.title("Categorieën")
    gui.write("Dit is een test.")
    gui.write("Dat zal toch niet kunnen, zeker?")
    gui.stop()
    gui.frame("frametitel", "En ik zei dit:", "KLOKO", "Zonder dat ik antwoord krreeg!!")
    print(gui.colors("red", "tEST"))
    print(gui.colors("magenta", "MAGEMTA"))
    print(gui.colors("cyan", "no color"))
    gui.yesNo("Testen?", lambda: print("Good!"), lambda: print("Fuck")) # lambda function
    gui.listPrompt("Welke actie wil je uitvoeren?", [["Een budget openen", lambda: print("one")], 
                                                     ["Een nieuw budget maken", lambda: print("two")], 
                                                     ["Een budget verwijderen", lambda: print("three")]])