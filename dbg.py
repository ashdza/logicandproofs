# Exports:
# debugging(level): turn on or off all dbg stuff, or selectively enable
# @TraceCalls() - decorator to trace entry & exit
# debug(obj) - indented display of obj (returns obj, so can be used as "tap")
# check(aLambda) - if aLambda does not evaluate to True, print error

# Freely borrowed & adapted from others' code, sorry I did not keep track

import inspect
import logging
import sys
from functools import wraps
import pprint
from enum import Enum


class Dbg(Enum):
    all = "All"
    none = "Off"
    enabled_only = "Enabled_Only"


DEBUGGING = Dbg.all


def debugging(level: Dbg):
    global DEBUGGING
    DEBUGGING = level


def is_visible(enabled):
    return DEBUGGING is Dbg.all or (DEBUGGING is Dbg.enabled_only and enabled)


class TraceCalls(object):
    """ Use as a decorator on any function(s) to trace call & return values.
    """

    cur_indent = 0

    def __init__(self, enabled=False):
        self.indent_step = 1
        self.show_ret = True
        self.enabled = enabled

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            argstr = ', '.join(
                [repr(a) for a in args] +
                ["%s=%s" % (a, repr(b)) for a, b in kwargs.items()])
            msg = f">> {fn.__name__}({argstr})"
            _debug(msg, frame_index=2, traced=True, enabled=self.enabled)

            TraceCalls.cur_indent += self.indent_step
            ret = fn(*args, **kwargs)
            TraceCalls.cur_indent -= self.indent_step

            if self.show_ret:
                _debug('<< %s' % str(ret), frame_index=2, traced=True, enabled=self.enabled)
            return ret
        return wrapper if is_visible(self.enabled) else fn


def _pp_indent(obj, indent=0, prefix=""):
    fstring = ' ' * indent + prefix + ' {}'
    lines = pprint.pformat(obj).splitlines(True)
    return ''.join([lines[0]] + [fstring.format(l) for l in lines[1:]])


def debug(obj, label="", pretty=False, enabled=False):
    """Display with indentation for debugging, returns obj. Optional label
    and multi-line pretty-printing args, and enabled for selective debugging."""
    return _debug(obj, label=label, pretty=pretty, enabled=enabled, frame_index=2)


logging.basicConfig(format='%(message)s', level=0)


def _debug(obj, label="", frame_index=1, traced=False, pretty=False, checked=None, enabled=False):
    """Internal use with additional args"""
    if not is_visible(enabled):
        return obj
    YELLOW, GREEN, RED, RESET = "\u001b[33m", "\u001b[1;32m", "\u001b[1;31m", "\u001b[0m"
    COLOR = YELLOW if checked is None else GREEN if checked is True else RED
    frame, filename, line_number, function_name, lines, index = inspect.getouterframes(
        inspect.currentframe())[frame_index]
    line = lines[0]
    call_level = TraceCalls.cur_indent
    tab_level = 0 if traced else line.find(line.lstrip()) // 4
    call_padding = ' | ' * call_level
    tab_padding = '  ' * tab_level
    msg = _pp_indent(obj, indent=3, prefix=call_padding + tab_padding) if pretty else str(obj)
    lbl = f"{label}: " if label else ""
    logging.debug(f"{YELLOW}{line_number:<3d}{call_padding}{tab_padding} {COLOR}{lbl}{msg}{RESET}")
    sys.stdout.flush()
    sys.stderr.flush()
    return obj


def check(msg, a_lambda, enabled=True):
    """If a_lambda() is False display FAILED message"""
    if not is_visible(enabled):
        return
    if not a_lambda():
        _debug(f"FAILED {msg} <<<<<<<<<<<<<<<<<<<<<<<<<<", frame_index=2, checked=False, enabled=enabled)
    else:
        _debug(f"PASSED {msg}", frame_index=2, checked=True, enabled=enabled)

