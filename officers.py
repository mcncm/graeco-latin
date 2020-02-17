import z3

def to_greek(ref: z3.IntNumRef):
    """Turns an integer offset 0 <= ref < size into a corresponding lowercase Greek
    character.
    """
    ALPHA_ORD = 945
    return chr(ref.as_long() + ALPHA_ORD)

def to_latin(ref: z3.IntNumRef):
    """Turns an integer offset 0 <= ref < size into a corresponding lowercase Latin
    character.
    """
    A_ORD = 97
    return chr(ref.as_long() + A_ORD)


class GLSolver:

    def __init__(self, size: int):
        s = z3.Solver()
        officers = [[(z3.Int(f'g_{i}_{j}'), z3.Int(f'l_{i}_{j}'))
                for i in range(size)]
                for j in range(size)]

        # symbol constraint
        for row in officers:
            for greek, latin in row:
                s.add(greek >= 0)
                s.add(greek < size)

                s.add(latin >= 0)
                s.add(latin < size)

        # uniqueness and completeness constraints
        for i, row in enumerate(officers):
            for j, (greek, latin) in enumerate(row):
                for k, _row in enumerate(officers):
                    for l, (_greek, _latin) in enumerate(_row):
                        # uniqueness
                        if i != k or j != l:
                            s.add(z3.Or(greek != _greek, latin != _latin))
                        # completeness
                        if ((i == k) and (j != l)) or ((i != k) and (j == l)):
                            s.add(z3.And(greek != _greek, latin != _latin))

        self.size = size
        self.officers = officers
        self.solver = s

    def pprint(self, gl_chars: bool = False):
        """Pretty-print a solution of the Graeco-Latin square.
        """
        try:
            self.solver.check()
            model = self.solver.model()
            for row in self.officers:
                line = ''
                for greek, latin in row:
                    if gl_chars == True:
                        line += '({}, {})  '.format(
                            to_greek(model[greek]),
                            to_latin(model[latin])
                        )
                    else:
                        line += '({}, {})  '.format(
                            str(model[greek].as_long() + 1),
                            str(model[latin].as_long() + 1)
                        )
                print(line)
        except Exception:
            print("This model is unsatisfiable!")

