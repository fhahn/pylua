"""
"""
import pytest

from luna.w_objects import W_Pri, W_Num, W_Str
from luna.module import ModuleDef
from luna.modules.patterns import find2, compile_re


StringModule = ModuleDef('string')


def handle_args(args):
    s = args[0].s_val
    start = 0
    plain = False
    expr = compile_re(args[1].s_val, plain)

    if len(args) > 2:
        start = args[2].n_val - 1
        if len(args) > 3:
            w_pri = args[3]
            assert isinstance(w_pri, W_Pri)
            plain = w_pri.is_true()
    return s, expr, start, plain


@StringModule.function('find')
def method_find(args):
    s, expr, start, plain = handle_args(args)
    matches = next(find2(expr, s, start))
    if matches == (-1, -1):
        return [W_Pri(0)]
    else:
        return [W_Num(matches[0]), W_Num(matches[1])]


@StringModule.function('match')
def method_match(args):
    s, expr, start, plain = handle_args(args)
    start_i, stop_i = next(find2(expr, s, start))
    if (start_i, stop_i) == (-1, -1):
        return [W_Pri(0)]
    else:
        return [W_Str(s[start_i-1:stop_i])]


@StringModule.function('gsub')
def method_gsub(args):
    s = args[0].s_val
    pattern = args[1].s_val
    replace = args[2].s_val
    expr = compile_re(pattern, False)
    sublist = []
    last_stop = 0
    for m_start, m_stop in find2(expr, s, 0):
        if (m_start, m_stop) == (-1, -1):
            return [W_Str(s)]
        else:
            sublist.append(s[last_stop:m_start-1])
            sublist.append(replace)
            last_stop = m_stop
    sublist.append(s[last_stop:])
    res = "".join(sublist)
    return [W_Str(res)]
