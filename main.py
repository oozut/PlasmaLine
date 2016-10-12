from Level.Level import Levels
from Line.Line import Lines

levels = Levels('data/CI.level')
lines  = Lines('data/CI.line')

levels.linesimport(lines)

#for level in levels.levels_obj:
#    print 'The chemical configuration is {0} and the term is {1}.'.format(level.configuration, level.level)
    #print 'The configuration is {1} and the level is {2}'.format(level.configuration, str(level.level))

levels.GroupingProcedure(levels.grouping_method_1)


print(len(levels.grouped_levels))
#for group in levels.grouped_levels:
#    print(group.level)

