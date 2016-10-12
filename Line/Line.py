

class Lines:
    """
    Class for the Lines of a atomic species

    The class should contains all the information about the line using the NIST notation : http://physics.nist.gov/PhysRefData/ASD/lines_form.html

    """
    def __init__(self,name_file):
        """
        The function that initialise the object using the ASCII formatted return from the NIST database

        :param name_file: the name of the file that is used to create the first database for the classification of the line of a spectra

        """

        file = open(name_file,'r') # read the file

        f = open(name_file, 'r')  # read the file
        self.lines_obj = []  # the list for the objects
        for line in f.readlines()[5:]:
            list_line= line.split('|')
            if not (len(list_line)== 1) and not list_line[0][0] == '-':
                if not (list_line[0].strip() == list_line[3].strip()):
                    self.lines_obj.append(Line(list_line[3].strip(), list_line[6].strip(), list_line[7].strip(),
                                               list_line[8].strip(), list_line[9].strip(), list_line[10].strip(),
                                               list_line[11].strip(), list_line[12].strip()))
            else:
                exit


class Line:
    """
    Class for the Lines of a atomic species

    The class should contains all the information about the line using the NIST notation : http://physics.nist.gov/PhysRefData/ASD/lines_form.html

    """
    def __init__(self,A,EiEk,ConfLow,TermLow,JLow,ConfUp,TermUp,JUp):
        """
        The initialisation for the Line
        """
        self.A = float(A)
        Level = EiEk.split('-')
        bad_characters = '[]()<>'  # type of characters founds in the NIST database
        level = Level[0].translate(None, bad_characters)
        self.Ei = float(level)
        level = Level[1].translate(None, bad_characters)
        self.Ek = float(level)
        self.ConfLow = ConfLow
        self.TermLow = TermLow
        self.JLow = JLow
        self.ConfUp = ConfUp
        self.TermUp = TermUp
        self.JUp = JUp