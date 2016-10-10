class Levels:
    """
    Class for the Levels of a atomic species
    The class should contains all the information about the line using the NIST notation :
    http://physics.nist.gov/PhysRefData/ASD/lines_form.html
    """
    def __init__(self, name_file):
        """
        The function that initialise the object using the ASCII formatted return from the NIST database
        :param name_file: the name of the file that is used to create the first database for the classification of the
        line of a spectra
        """
        f = open(name_file, 'r')  # read the file
        self.levels_obj = []  # the list for the objects
        for line in f.readlines():
            list_line= line.split('|')
            if not(list_line[0].strip() == list_line[3].strip()):  # Ignore the line that does not contains information
                # about the level
                if not(list_line[0].strip() == ''):
                    level = Level(list_line[0].strip(), list_line[1].strip(), list_line[2].strip(), list_line[3].strip())
                else:
                    level = Level(self.levels_obj[-1].configuration, list_line[1].strip(), list_line[2].strip(), list_line[3].strip())
                level.configuration_strip_down()
                self.levels_obj.append(level)


            #print(line.split('|'))



class Level:
    """
    Class for the level of a atomic species

    The class should contains all the information about the line using the NIST notation : http://physics.nist.gov/PhysRefData/ASD/lines_form.html

    """

    def __init__(self, configuration, term, parity, level):
        """
        A single level for an atomic specy

        :param configuration: the electronic configuration of the level
        :param term: the term of the level
        :param J: the parity of the level
        :param level: the energy of the level
        """
        self.configuration = configuration
        self.term = term
        self.J = parity
        self.level = float(level)


        self.configuration_high_detail = [] ## the high detail for the configuration

    def configuration_strip_down(self):

        list_config = self.configuration.split('.')
        new_config = []
        for config in list_config:
            if(len(config)==2):
                new_config.append([config[0:2],1])  # the new configuration provide information about the electronic
                # level ('2p,3d,4f') in the first element of the list and the number of electrons in the electronic
                # level.
            else:
                new_config.append([config[0:2],config[2]])  # the new configuration provide information about the
                # electronic level ('2p,3d,4f') in the first element of the list and the number of electrons in the
                # electronic level.
        self.configuration_high_detail = new_config