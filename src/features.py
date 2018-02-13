import json

def get_features():
    if get_features.features == {}:
        f = open('features.json', 'r')
        features = json.load(f)
    return features
get_features.features = {}
