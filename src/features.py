from parser import parse
import json

###
# tag_sounds
#
# Given a set of sounds, tag them with the appropriate place, manner, and
# voicing tags.
def tag_sounds(sounds):
    for k in place_constraints:
        c = parse(place_constraints[k])

        cs = constrained_sounds(sounds, c)
        for s in cs:
            sounds[s]['place'] = k

    for k in manner_constraints:
        c = parse(manner_constraints[k])

        cs = constrained_sounds(sounds, c)
        for s in cs:
            sounds[s]['manner'] = k

    return sounds

###
# get_sounds
#
# Get the set of sounds from the sounds.json file, tags them via
# tag_sounds, and returns them. Memoizes the set of sounds.
def get_sounds(tag = True):
    if get_sounds.sounds == {}:
        f = open('features.json', 'r')
        sounds = json.load(f)
        if tag:
            sounds = tag_sounds(sounds)
    return sounds
get_sounds.sounds = {}

###
# constrained_sounds
#
# Given a set of sounds, return the set that satisfies the constraint.
def constrained_sounds(sounds, constraint):
    s = {}
    for k in sounds:
        if constraint.constrain(sounds[k]):
            s[k] = sounds[k]
    return s

###
# all_constrained_sounds
#
# Equivalent to calling constrained_sounds(get_sounds()).
def all_constrained_sounds(constraint):
    return constrained_sounds(get_sounds(), constraint)

###
# place_constraints
#
# A set of constraints that map directly from major class to phonetic place.
place_constraints = {
    'Bilabial': '[] => [+labial, -labiodental, -syllabic]',
    'Labiodental': '[] => [+labial, +labiodental, -syllabic]',

    'Dental': '[] => [+coronal, +anterior, +distributed, -dorsal, -syllabic]',
    'Alveolar': '[] => [+coronal, +anterior, -distributed, -syllabic]',
    'Postalveolar': '[] => [+coronal, -anterior, +distributed, -syllabic]',
    'Retroflex': '[] => [+coronal, -anterior, -distributed, -syllabic]',

    'Alveolopalatal': '[] => [+coronal, +anterior, +distributed, +dorsal, -syllabic]',
    'Palatal': '[] => [+coronal, +dorsal, -anterior, -syllabic]',

    'Velar': '[] => [-coronal, +dorsal, +high, -syllabic]',
    'Uvular': '[] => [+dorsal, -high, -low, -syllabic]',
    'Pharyngeal': '[] => [+dorsal, +low, -syllabic]',
    'Glottal': '[] => [-labial, -coronal, -dorsal, -syllabic]'
}

###
# manner_constraints
#
# A set of constraints that map directly from major class to phonetic manner.
manner_constraints = {
    'Plosive': '[] => [-sonorant, -continuant, -delayed release]',
    'Affricate': '[] => [-sonorant, -continuant, +delayed release]',
    'Fricative': '[] => [-sonorant, +continuant, -lateral]',

    'Lateral Fricative': '[] => [-sonorant, +continuant, +lateral]',

    'Nasal': '[] => [+nasal]',
    'Tap': '[] => [+tap]',
    'Trill': '[] => [+trill]',

    'Approximant': '[] => [+approximant, +consonantal, -lateral, -tap, -trill]',
    'Lateral Approximant': '[] => [+approximant, +consonantal, +lateral, -tap, -trill]',

    'Glide': '[] => [-syllabic, -consonantal]',

    'Vowel': '[] => [+syllabic]'
}
