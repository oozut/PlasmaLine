import re

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
        list_level = []
        list_level_bool = False
        for line in f.readlines()[3:]:
            list_line= line.split('|')
            if not (len(list_line)== 1) and not list_line[0][0] == '-':
                if not(list_line[0].strip() == list_line[3].strip()):  # Ignore the line that does not contains information
                    # about the level
                    if (list_line[3].strip() == ''):
                        list_level.append([list_line[0].strip(), list_line[1], list_line[2].strip(),
                                           list_line[3].strip()])
                        list_level_bool = True
                    else:
                        if list_level_bool:
                            for l in list_level:
                                self.levels_obj.append(Level(list_level[0][0], l[1], l[2], list_line[3].strip()))
                            self.levels_obj.append(Level(list_level[0][0], list_line[1].strip(), list_line[2].strip(),
                                list_line[3].strip()))
                            list_level_bool = False
                            list_level = []
                        else:
                            if not(list_line[0].strip() == ''):
                                level = Level(list_line[0].strip(), list_line[1].strip(), list_line[2].strip(),
                                list_line[3].strip())
                            else:
                                level = Level(self.levels_obj[-1].configuration, list_line[1].strip(),
                                              list_line[2].strip(),list_line[3].strip())
                            level.configuration_strip_down()
                            self.levels_obj.append(level)
            else:
                exit

    def linesimport(self,Lines):

        for line in Lines.lines_obj:
            for level in self.levels_obj:
                if(level.configuration == line.ConfLow and level.term == line.TermLow and level.J == line.JLow):
                    level.add_transition_gain(line)
                if (level.configuration == line.ConfUp and level.term == line.TermUp and level.J == line.JUp):
                    level.add_transition_loss(line)


    def grouping_procedure(self,function):
        grouped_level = function(self.levels_obj)

        self.grouped_levels = grouped_level

    def grouping_method_1(self,all_levels):
        '''
        The grouping method 1 is the following:
            The electronic level with the same chemical configuration are grouped together into on equivalent level.
            Finally, the new level can be splitted if the energy between the maximum and the minimum is higher than 2%
            difference.
        :param all_levels: all the level
        :return: the new chemical configuration with the fictitious levels calculated with the grouping procedure.
        '''
        new_grouped_level = []
        working_levels = all_levels
        for level in working_levels:  # the ground level is extracted before any reconfiguration
            if(level.level == 0.):
                new_grouped_level.append(FictitiousLevel(level.configuration,level.term,level.J,level.level))
                working_levels.remove(level)  # I remove the ground level from the list
                break

        for level in working_levels:  # remove the ionisation state
            if(level.term == 'Limit'):
                working_levels.remove(level)

        working_directory = {}
        for level in working_levels:  # Creation of the dictionary of chemical configuration.
            try:
                working_directory[level.configuration].append(level)
            except KeyError:
                working_directory[level.configuration] = []
                working_directory[level.configuration].append(level)

        fine_grouped_levels = []  # The fine grouping for the difference of energy no more than 5%
        for group_levels in working_directory.itervalues():
            n_gr = []
            for level, i in zip(group_levels, range(len(group_levels))):
                if i == 0:
                    l_gr = group_levels[0].level
                    n_gr.append(level)
                else:
                    if (level.level - l_gr)/l_gr > 0.05:
                        fine_grouped_levels.append(n_gr)
                        n_gr = []
                        n_gr.append(level)
                    else:
                        n_gr.append(level)
            fine_grouped_levels.append(n_gr)

        return fine_grouped_levels






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
        bad_characters = '[]()<>'  # type of characters founds in the NIST database
        level = level.translate(None, bad_characters)
        self.level = float(level)
        self.configuration_high_detail = []  # the high detail for the configuration
        self.transition_loss = []
        self.transition_gain = []

    def configuration_strip_down(self):

        list_config = self.configuration.split('.')
        new_config = []
        for config in list_config:
            head = config.rstrip('1234567890')
            if(len(config)==head):
                new_config.append([head, 1])  # the new configuration provide information about the electronic
                # level ('2p,3d,4f') in the first element of the list and the number of electrons in the electronic
                # level.
            else:
                new_config.append([head, config[len(head):]])  # the new configuration provide information about the
                # electronic level ('2p,3d,4f') in the first element of the list and the number of electrons in the
                # electronic level.
        self.configuration_high_detail = new_config

    def add_transition_loss(self,line):
        self.transition_loss.append(line)

    def add_transition_gain(self,line):
        self.transition_gain.append(line)


class FictitiousLevel(Level):

    def __init__(self,list_level,configuration = '', term = '', parity = '', level = '0.'):
        Level.__init__(self,configuration, term, parity, level)
        self.real_levels = list_level
        self.weight = 0.


    def calculate_weight(self):
        for level in self.real_levels:
            self.weight = 2*float(level.J)+1.

    def calculate_level(self):
        for level in self.real_levels:
            self.level = (2*float(level.J) + 1)*level.level  # the calculation for the fictutious level of energy
        self.level /= self.weight  # normalisation of the energy level