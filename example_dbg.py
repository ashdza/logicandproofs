# An example of using dbg: recursive calls, trace, debug, check

from dbg import debug, check, TraceCalls, debugging, Dbg

debugging(Dbg.all)


@TraceCalls()
def foo():
    debug('foo: Hi World', label="LABEL")
    debug("foo: well")
    for i in range(3):
        debug("foo: Now we're cookin")
        check(f"invariant: {i} < 2", lambda: i < 2)
        for i in range(debug(1, label="ONE")):
            debug("foo: 2 tabs in", enabled=True)
    return "42"


pp_stuff = ['spam', 'eggs', 'lumberjack', 'knights', 'ni']
pp_stuff.insert(0, pp_stuff[:])


@TraceCalls(enabled=True)
def bar(i, j=None):
    debug("bar " + str(i))
    debug(pp_stuff, pretty=False)
    if i > 1:
        bar(i - 1)
        return "99", i
    else:
        debug(pp_stuff, pretty=True)
        return foo(), i


if __name__ == '__main__':
    bar(3)

