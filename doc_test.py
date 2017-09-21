# code to test docstrings

class ClassTest(object):
    """Class Test lets me play with
       documentation standards in python
    """

    def __init__(self, name, number):
        """Initilize object with two arguments
               The goal of this method is to set
               up an object with some predefined
               variables used by all the methods
            Args:
                name (str):  The name of the object
                number(int):  A number for the object
        """
        self.name = name  # what happens to a comment here
        self.number = number
        """what about this"""

    def show(self):
        """Prints Name and Number of Object
                This is a really simple method.
        """

        print ("Hi, I am {}.  I am also number {}."
               .format(self.name, self.number))

    def get_info(self, arg):
        """Returns values. Not very useful except as test
               arg = "all" returns [True, name, number]
               arg = "name" returns [True, name, -1]
               arg = "number" returns [True, "", number]
               arg = "anything else" returns [False, "Arg Error", arg]
            Args:
                arg (str):  arg = "all" | "name" |"number"
            Returns:
                list: [True, str, int] or [False, str, str]
        """
        if arg == "all":
            return [True, self.name, self.number]
        elif arg == "name":
            return [True, self.name, -1]
        elif arg == "number":
            return [True, "", self.number]
        else:
            return [False, "Arg Error", arg]

if __name__ == "__main__":
    tester = ClassTest("Kevin", 6)
    tester.show()
    a = tester.get_info("all")
    print(a)