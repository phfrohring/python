# -*- coding: utf-8 -*-

from tools_09d3 import link

def test_impl():
    """Test link"""

    def one():
        return 1

    def two():
        return 2

    def add(one, two):
        return one + two

    def side_effect(add):
        # Some side effect.
        pass

    result = link([one,two,add,side_effect], {})

    assert result["add"] == 3
