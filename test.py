

a, b, c = (-60,2), (3,4), (4,5)

print("a = {}, b = {}, c = {}".format(*[tuple(value // -15 for value in t) for t in [a, b, c]]))