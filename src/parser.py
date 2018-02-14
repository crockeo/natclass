from parsy import * # alt, regex, string
import models

###
# _merge_dicts
def __merge_dicts(*args):
    d = {}
    for a in args:
        for k in a:
            d[k] = a[k]
    return d

###
# feature_parser
feature_parser = seq(
    alt(
        string('+'),
        string('-'),
        string('0')
    ),
    regex('\\w+').sep_by(whitespace).combine(lambda *args: ' '.join(args))
).combine(lambda value, feature:
    { feature: value }
)

###
# class_parser
class_parser = string('[').then(
    feature_parser.sep_by(
        string(',').skip(whitespace.optional())
    )
).skip(string(']')).combine(__merge_dicts)

###
# negative_parser
negative_parser = string('*').then(
    class_parser
).map(
    lambda d: models.NegativeConstraint(d)
)

###
# implicational_parser
implicational_parser = seq(
    class_parser << whitespace.optional() << string('=>') << whitespace.optional(),
    class_parser
).combine(
    lambda c1, c2: models.ImplicationalConstraint(c1, c2)
)

# Parsing out a string into a constraint, either Negative or Implicational.
# This function requires a string input.
def parse(s):
    return (negative_parser | implicational_parser).parse(s)
