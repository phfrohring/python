# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------------
# interface

__all__ = [ "link" ]

def link(transformations, state):
    """Apply a sequence of transformations to a state.

    Parameters
    ----------
    transformations : [transform …]
        Where ``transform ≡ function``.
    state : dict
        A dictionnary to which transforms are applied.

    Returns
    -------
    state
        The state after all transformations have been applied to it.

    Notes
    -----
    Assume::

        def one():
            return 1

        def two():
            return 2

        def add(one, two):
            return one + two

        def side_effect(add):
            print(add)

        result = link([one,two,add,side_effect], {})

    Conclude::

        result = { 'one': 1, 'two': 2, 'add': 3 }
    """
    return _link(transformations, state)

# --------------------------------------------------------------------------------
# implementation

from inspect import signature
import logging
logger = logging.getLogger(__name__)

def _link(transformations, state):
    for func in transformations:
        name_func = func.__name__
        keys = tuple(p for p in signature(func).parameters)

        logger.debug(f"state = {state}")
        logger.debug(f"{keys} → {name_func}")

        try:
            params = tuple(state[key] for key in keys)
        except KeyError as e:
            msg = f"""
  Expected: key is present in state so that func can be called.
  Actual: key is missing.
    key: {e.args[0]}
    func: {name_func}{str(keys)}
    state: {state}"""
            raise AssertionError(msg)

        result = func(*params)
        if result is not None:
            state[name_func] = result

    return state
