#!/usr/bin/env python3

from parser import parse

import features
import models
import server
import sys

###
# old_mode
#
# The way things used to work! Just prints out a class that was selected by
# some default options.
def old_mode():
    only_plosive = parse('[] => [-continuant, -sonorant, -delayed release]')
    only_voiceless = parse('*[+voice]')

    sc = models.SetConstraint(map(parse, [
        '[] => [-continuant, -sonorant, -delayed release]',
        '*[+voice]'
    ]))

    sc = models.SetConstraint([
        only_plosive,
        only_voiceless
    ])

    l = features.constrained_sounds(features.get_sounds(), sc)
    l.sort()
    for k in l:
        print(k)

###
# interactive_mode
#
# Repeatedly queries the user for constraints, returns the set of sounds that
# abide them.
def interactive_mode():
    sc = models.SetConstraint()
    while True:
        descriptor = input("> ")
        if descriptor == "exit":
            break
        elif descriptor == "clear":
            sc.clear()
        else:
            try:
                constraint = parse(descriptor)
                sc.add(constraint)
            except Exception as err:
                print('Could not parse constraint:')
                print(err)
                continue

            l = features.constrained_sounds(features.get_sounds(), sc)
            print(l)
            for k in l:
                print(k)

def main(args):
    if len(args) >= 2 and args[1] == 'oldmode':
        old_mode()
    elif len(args) >= 2 and args[1] == 'server':
        server.start()
    else:
        interactive_mode()

if __name__ == '__main__':
    main(sys.argv)
