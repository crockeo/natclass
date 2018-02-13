# A constraint of the form *[ (class) ]
class NegativeConstraint:
    def __init__(self, _natclass):
        self.natclass = _natclass

    def constrain(self, sound):
        for v in self.natclass:
            if sound[v] == self.natclass[v]:
                return False
        return True

# A constraint of the form [ (class1) ] => [ (class2) ]
class ImplicationalConstraint:
    def __init__(self, _selectclass, _implyclass):
        self.selectclass = _selectclass
        self.implyclass = _implyclass

    def constrain(self, sound):
        satselect = True
        for v in self.selectclass:
            if sound[v] != self.selectclass[v]:
                satselect = False
                break

        if satselect:
            for v in self.implyclass:
                if sound[v] != self.implyclass[v]:
                    return False

        return True

# A set of Negative and Implicational Constraints to create a combinative set of
# constraints.
class SetConstraint:
    def __init__(self, __constraints=[]):
        self.constraints = __constraints

    def add(self, constraint):
        self.constraints.add(constraint)

    def constrain(self, sound):
        for constraint in self.constraints:
            if not constraint.constrain(sound):
                return False
        return True
