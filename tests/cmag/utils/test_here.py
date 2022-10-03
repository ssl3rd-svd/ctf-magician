import pytest

from cmag.utils.here import *

def test_here_init():
    here = Here('hi')
    assert here.hello == 'hi'

def test_here_func1():
    here = Here('hi')
    assert here.func1(1, 2) == 3