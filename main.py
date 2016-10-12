from Level.Level import Levels
from Line.Line import Lines

levels = Levels('data/CI.level')
lines  = Lines('data/CI.line')

levels.linesimport(lines)

levels.grouping_procedure(levels.grouping_method_1)

for group in levels.grouped_levels:
    print(group)

