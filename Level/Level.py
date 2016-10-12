from operator import attrgetter
import matplotlib.pyplot as plt

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
        self.ground_level = Level('', '', '', '0.')  # the ground levels for future use
        self.ionisation_levels = []  # the ionisation level
        self.grouped_levels = [] # the list for the new grouped levels
        list_level = []
        list_level_bool = False
        for line in f.readlines()[3:]:
            list_line= line.split('|')
            if not (len(list_line)== 1) and not list_line[0][0] == '-':
                if not(list_line[0].strip() == list_line[3].strip()):  # Ignore the line that does not contains information
                    # about the level
                    if (list_line[3].strip() == ''):
                        list_level.append([list_line[0].strip(), list_line[1].strip(), list_line[2].strip(),
                                           list_line[3].strip()])
                        list_level_bool = True
                    else:
                        if list_level_bool:
                            for l in list_level:
                                self.levels_obj.append(Level(list_level[0][0], list_level[0][1], l[2], list_line[3].strip()))
                            self.levels_obj.append(Level(list_level[0][0], list_level[0][1], list_line[2].strip(),
                                list_line[3].strip()))
                            list_level_bool = False
                            list_level = []
                        else:
                            if not(list_line[0].strip() == ''):
                                level = Level(list_line[0].strip(), list_line[1].strip(), list_line[2].strip(),
                                list_line[3].strip())
                            else:
                                level = Level(self.levels_obj[-1].configuration, self.levels_obj[-1].term,
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


    def GroupingProcedure(self, function):
        ''' This methods is used to group level together and check the validity of the grouping

        The grouping is check by compared the number of real level with the number of level used in the fictitious level

        :param function: the function use for the GroupingProcedure
        :type function: Levels.methods
        :return: No return
        '''
        grouped_level = function(self.levels_obj)

        self.grouped_levels = grouped_level

        number_of_level = 0
        for ficLevel in grouped_level:
            number_of_level += len(ficLevel.list_real_levels)

        if not number_of_level == (len(self.levels_obj) + len(self.ionisation_levels) + 1):
            print 'Error with the number of levels from the fictitious level'
            print 'Number of real level in fictitious Level is {0} and the number of level from the reading {1}'\
                .format(number_of_level, len(self.levels_obj) + len(self.ionisation_levels) + 1)

        fig = plt.figure(figsize=(12, 10))
        ax = plt.subplot(111)
        size_label = 28.
        plt.rc('text', usetex=True)
        ax.tick_params(which='major', direction='out', width=1.)
        ax.tick_params(which='minor', direction='out', width=0.5)
        ax.grid(True, linestyle='-', linewidth=0.5, alpha=0.05, which='minor')
        ax.grid(True, linestyle='-', linewidth=1., alpha=0.15, which='major')
        plt.minorticks_on()
        plt.title(r'Old and Grouped Fictitious Electronic configuration',size = size_label)
        #plt.xlabel(r'Radial distance [\textmu m]', size=size_label)
        plt.ylabel(r'Energy Level [eV]', size=size_label)
        plt.xticks(fontsize=size_label)
        plt.yticks(fontsize=size_label)
        x_new = [2, 2.5]
        x_old = [0.5, 1.]
        for ficLevel in grouped_level:
            plt.plot(x_new, [ficLevel.level, ficLevel.level], 'b-', lw=2.)
            for realLevel in ficLevel.list_real_levels[:20]:
                plt.plot(x_old, [realLevel.level, realLevel.level], 'g-', lw=2.)
                ax.annotate("",
                            xy=(x_new[0], ficLevel.level), xycoords='data',
                            xytext=(x_old[1], realLevel.level), textcoords='data',
                            arrowprops=dict(arrowstyle="->",  # linestyle="dashed",
                                            color="0.5",
                                            connectionstyle="arc,angleA=0,angleB=180,armA=10,armB=10,rad=5",
                                            ),
                            )
        for level in self.ionisation_levels:
            plt.axhline(y=level.level, color='r', lw=2., linestyle='--')
        # plt.plot(numb,shift_u[:,0],'m-',lw=3.)
        fname = 'electronic_configuration' + '.pdf'
        #print 'The figure is ready'
        #plt.ylim(8,11)
        fig.tight_layout()
        fig.savefig(fname)
        plt.close(fig)


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
            # print 'The chemical configuration is {0} and the term is {1}, and level is {2}.'
            # .format(level.configuration, level.term, level.level)
            if level.level == 0. :
                new_grouped_level.append(FictitiousLevel([level], level.configuration, level.term, level.J, level.level))
                self.ground_level = level
        try:
            working_levels.remove(self.ground_level)  # It must be noted that the remove methods, delete the Level from
            # the self.levels_obj.
        except ValueError:
            print 'There is no grounds levels which is confusing, Please check your data'

        for level in working_levels:  # remove the ionisation state
            # print 'The chemical configuration is {0} and the term is {1}.'.format(level.configuration, level.term)
            if level.term == 'Limit' :
                self.ionisation_levels.append(level) # It must be noted that the remove methods, delete the Level from
            # the self.levels_obj.
        try:
            for level in self.ionisation_levels:
                working_levels.remove(level)
        except ValueError:
            print 'There is no ionisation levels which is confusing, Please check your data'

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
                        l_gr = level.level
                        n_gr.append(level)
                    else:
                        n_gr.append(level)
            fine_grouped_levels.append(n_gr)

        for grouped_level in fine_grouped_levels:
            new_grouped_level.append(FictitiousLevel(grouped_level, grouped_level[0].configuration))

        for level in new_grouped_level:
            level.calculate_level()

        new_grouped_level = sorted(new_grouped_level, key=attrgetter('level'))

        further_grouping = []  # the further grouping is used to group level with a energy level with a 2% difference
        # but different chemical configuration
        n_gr = []
        for level, i in zip(new_grouped_level, range(len(new_grouped_level))):
            if i == 0:
                l_gr = new_grouped_level[1].level
                further_grouping.append(level.list_real_levels)
                #for RealLev in new_grouped_level[1].list_real_levels:
                #    n_gr.append(RealLev)
            else:
                if (level.level - l_gr)/l_gr > 0.002:
                    further_grouping.append(n_gr)
                    n_gr = []
                    l_gr = level.level
                    for RealLev in level.list_real_levels:
                        n_gr.append(RealLev)
                else:
                    for RealLev in level.list_real_levels:
                        n_gr.append(RealLev)

        further_grouping.append(n_gr)

        last_grouped_level = []
        for group in further_grouping:
            last_grouped_level.append(FictitiousLevel(group))

        for fictitious_level in last_grouped_level:
            fictitious_level.calculate_level()

        last_grouped_level = sorted(last_grouped_level, key=attrgetter('level'))

        return last_grouped_level


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

    def __init__(self, list_level, configuration='', term='', parity='', level='0.'):
        if isinstance(level, str):
            Level.__init__(self,configuration, term, parity, level)
        else:
            Level.__init__(self, configuration, term, parity, str(level))

        self.list_real_levels = list_level
        self.weight = 0.
        self.level = 0.

    def calculate_weight(self):
        for level in self.list_real_levels:
            self.weight += 2.*float(level.J)+1.

    def calculate_level(self):
        self.calculate_weight()
        for level in self.list_real_levels:
            self.level += (2.*float(level.J) + 1)*level.level  # the calculation for the fictutious level of energy
        self.level /= self.weight  # normalisation of the energy level
