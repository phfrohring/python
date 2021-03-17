# -*- coding: utf-8 -*-

# Imports

from program_9ef5 import Instruction, Program

# Implementation


def test_impl():
    """docstring"""
    Instruction.clean()

    @Instruction
    def hello(hello):
        return "hello"

    @Instruction
    def world(world):
        return "world"

    @Instruction
    def concat(hello, world, hello_world):
        return f"{hello} {world}"

    assert Program(Instruction.all()).execute() == "hello world"
