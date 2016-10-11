

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
        self.levels_obj = []  # the list for the objects
        for line in f.readlines()[5:]:
            list_line= line.split('|')
            if not (len(list_line)== 1) and not list_line[0][0] == '-':
                print(list_line)
            else:
                exit


class Line:
    """
    Class for the Lines of a atomic species

    The class should contains all the information about the line using the NIST notation : http://physics.nist.gov/PhysRefData/ASD/lines_form.html

    """
    def __init__(self):
        """
        The initialisation for the Line
        """
        print('a')