import json

def get_features():
    if get_features.features == {}:
        f = open('features.json', 'r')
        features = json.load(f)
    return features
get_features.features = {}

###
# place_constraints
#
# A set of constraints that map directly from major class to phonetic place.
place_constraints = {
    'Bilabial': '[] => [+labial, -labiodental]',
    'Labiodental': '[] => [+labidal, +labiodental]',

    'Dental': '[] => [+coronal, +anterior, +distributed, -dorsal]',
    'Alveolar': '[] => [+coronal, +anterior, -distributed]',
    'Postalveolar': '[] => [+coronal, -anterior, +distributed]',
    'Retroflex': '[] => [+coronal, -anterior, -distributed]',
    'Alveolopalatal': '[+coronal, +anterior, +distributed, +dorsal]',

    'Palatal': '[] => [+coronal, +dorsal]',
    'Velar': '[] => [-coronal, +dorsal, +high]',
    'Uvular': '[] => [+dorsal, -high, -low]',
    'Pharyngeal': '[] => [+dorsal, +low]',
    'Glottal': '[] => [-labial, -coronal, -dorsal]'
}
