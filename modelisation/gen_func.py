def strip_methods(eq, libraries):
    break_chars = [" ", "+", "-", "/", "*"]
    for lib in libraries:
        while lib in eq:
            ob, cb = 0, 0
            start = eq.find(lib)
            slice1, slice2 = [start, 0], [0, 0]
            for i in range(start, len(eq)):
                if eq[i] == "(":
                    ob += 1
                    if ob == 1:
                        slice1[1] = i + 1
                elif eq[i] == ")":
                    cb += 1
                    if cb == ob:
                        slice2[0] = i
                        slice2[1] = i + 1
                        break
                elif eq[i] in break_chars or i == len(eq) - 1:
                    if ob == 0:
                        slice1[1] = i + 1
            if slice2[0] != 0:
                eq = (
                    eq[: slice1[0]]
                    + " " * (slice1[1] - slice1[0])
                    + eq[slice1[1] : slice2[0]]
                    + " " * (slice2[1] - slice2[0])
                    + eq[slice2[1] :]
                )
            else:
                eq = eq[: slice1[0]] + " " * (slice1[1] - slice1[0]) + eq[slice1[1] :]
    return eq


class Function:
    def __init__(self, equation, libraries):
        eq = equation[equation.find('=') + 1 :]

        self.stripped = strip_methods(eq, libraries)

        param_names = self.stripped[:].lower()
        for i in [" ", "*", "+", "/", "-", ".", ","]:
            param_names = param_names.replace(i, "")
        self.letters = list(set([i for i in param_names if not i.isdigit()]))

        if "x" in self.letters:
            del self.letters[self.letters.index("x")]
            self.unique_param_names = self.letters[:]
            self.unique_param_names.insert(0, "x")
        else:
            self.unique_param_names = self.letters[:]
        if len(self.unique_param_names) <= 1:
            self.no_fit = True
        else:
            self.no_fit = False
        param_names = ",".join(self.unique_param_names)

        exec("def func({}): return {}".format(param_names, eq), globals())
        self.real_func = func
        self.params = []

    def set_params(self, params):
        self.params = params

    def func(self, x):
        if len(self.unique_param_names) == 0:
            return self.real_func()
        elif len(self.unique_param_names) == 1:
            return self.real_func(x)
        else:
            return self.real_func(x, *self.params)
