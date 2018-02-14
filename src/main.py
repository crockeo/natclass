#!/usr/bin/env python3

from parser import parse

import features
import models

def all_sat(constraint):
    s = []
    f = features.get_features()
    for k in f:
        if constraint.constrain(f[k]):
            s.append(k)
    return s

def main():
    only_plosive = parse('[] => [-continuant, -sonorant, -delayed release]')
    only_voiceless = parse('*[+voice]')

    sc = models.SetConstraint([
        only_plosive,
        only_voiceless
    ])

    l = all_sat(sc)
    l.sort()
    for k in l:
        print(k)

if __name__ == '__main__':
    main()
