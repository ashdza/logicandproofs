import typing as T
forAll = all
exists = any

# (Not) all students are tired

Student = T.NamedTuple("Student", name=str, hrs=int)

Students = {Student("Bob", 3),
            Student("Ashley", 4),
            Student("Emily", 5)}

def is_tired(s: Student) -> bool:
    return s.hrs >= 3

assert forAll(is_tired(s) for s in Students)

# (not) some student works <5 hours
assert exists((lambda s: s.hrs < 5)(s) for s in Students)

# every number (in Nums) equals the negative of another number (in Nums)
Nums = {-3, -2, -1, 1, 2, 3}


def hasNeg(x):
    def isNeg(a, b):
        return a == -b
    return exists( isNeg(x, y) for y in Nums)

assert forAll( hasNeg(x) for x in Nums)