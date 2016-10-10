

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

        for line in file.readlines():


class Line:
    """
    Class for the Lines of a atomic species

    The class should contains all the information about the line using the NIST notation : http://physics.nist.gov/PhysRefData/ASD/lines_form.html

    """
    def __init__(self):
        """
        The initialisation for the Line
        """