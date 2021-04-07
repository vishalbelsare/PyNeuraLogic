from neuralogic.model.java_objects import get_java_factory


class Predicate:
    """WeightedPredicate"""

    def __init__(self, name, arity, private, special):
        self.name = name
        self.arity = arity
        self.private = private
        self.special = special

        self.java_object = get_java_factory().get_predicate(self)

    def set_arity(self, arity):
        if self.arity == arity:
            return self

    def to_str(self):
        special = "@" if self.special else ""
        private = "*" if self.private else ""
        return f"{private}{special}{self.name}"

    def __str__(self):
        special = "@" if self.special else ""
        private = "*" if self.private else ""
        return f"{private}{special}{self.name}/{self.arity}"