# -*- coding: utf-8 -*-

"""Verify sphinxcontrib.chapeldomain.ChapelDomain."""

from __future__ import print_function, unicode_literals

import mock
import unittest

from sphinxcontrib.chapeldomain import (
    ChapelDomain, chpl_sig_pattern, chpl_attr_sig_pattern)


class ChapelDomainTests(unittest.TestCase):
    """ChapelDomain tests."""

    def test_init(self):
        """Simple test to verify ChapelDomain can be initialized."""
        env = mock.Mock()
        env.domaindata = {'name': 'chapel'}
        self.assertIsNotNone(ChapelDomain(env))


class PatternTestCase(unittest.TestCase):
    """Helper methods for regex pattern tests."""

    def check_is_not_match(self, sig):
        """Verify sig does not match attr pattern."""
        match = self.pattern.match(sig)
        self.assertIsNone(match)


class SigPatternTests(PatternTestCase):
    """Verify chpl_sig_pattern regex."""

    pattern = chpl_sig_pattern

    def check_sig(self, sig, func_prefix, name_prefix, name, arglist, retann):
        """Verify signature results in appropriate matches."""
        match = self.pattern.match(sig)
        self.assertIsNotNone(match)

        (actual_func_prefix, actual_name_prefix, actual_name, actual_arglist, actual_retann) = match.groups()
        self.assertEqual(func_prefix, actual_func_prefix)
        self.assertEqual(name_prefix, actual_name_prefix)
        self.assertEqual(name, actual_name)
        self.assertEqual(arglist, actual_arglist)
        self.assertEqual(retann, actual_retann)

    def test_does_not_match(self):
        """Verify various signatures that should not match."""
        test_cases = [
            '...',
            '.',
            ':fda',
            '@',
            '#',
        ]
        for sig in test_cases:
            self.check_is_not_match(sig)

    def test_no_parens(self):
        """Verify various symbols (e.g. parenless functions) parse."""
        test_cases = [
            'x',
            'foo',
            'l_l',
            'foo123',
            '1',
            '123',
            '+',
            '-',
            '/',
            '*',
            '**',
        ]
        for sig in test_cases:
            self.check_sig(sig, None, None, sig, None, None)

    def test_no_args(self):
        """Verify various functions with no args parse correctly."""
        test_cases = [
            ('x()', 'x'),
            ('foo()', 'foo'),
            ('l_l()', 'l_l'),
            ('foo123()', 'foo123'),
            ('1()', '1'),
            ('123()', '123'),
            ('+()', '+'),
            ('-()', '-'),
            ('/()', '/'),
            ('*()', '*'),
            ('**()', '**'),
            ('x ()', 'x'),
        ]
        for sig, name in test_cases:
            self.check_sig(sig, None, None, name, '', None)

    def test_with_args(self):
        """Verify function signatures with arguments parse correctly."""
        test_cases = [
            ('x(y)', 'x', 'y'),
            ('x(y:int)', 'x', 'y:int'),
            ('x(y:int=1)', 'x', 'y:int=1'),
            ('x( y : int = 1 )', 'x', ' y : int = 1 '),
            ('x ( y )', 'x', ' y '),
            ('x ( )', 'x', ' '),
            ('+(a:string, b:string)', '+', 'a:string, b:string'),
            ('+ (a, b)', '+', 'a, b'),
            ('++++++++++++++++++++ ( +++ )', '++++++++++++++++++++', ' +++ '),
        ]
        for sig, name, arglist in test_cases:
            self.check_sig(sig, None, None, name, arglist, None)

    def test_with_return_type(self):
        """Verify function signatures with return types parse correctly."""
        test_cases = [
            ('x(): int', 'x', '', 'int'),
            ('x(): MyMod.MyClass', 'x', '', 'MyMod.MyClass'),
            ('x(): int(32)', 'x', '', 'int(32)'),
            ('x():int(32)', 'x', '', 'int(32)'),
            ('x(y:int(64)):int(32)', 'x', 'y:int(64)', 'int(32)'),
            ('x(y:int(64), d: domain(r=2, i=int, s=true)): [{1..5}] real', 'x', 'y:int(64), d: domain(r=2, i=int, s=true)', '[{1..5}] real'),
            ('x(): domain(1)', 'x', '', 'domain(1)'),
            ('x(): [{1..n}] BigNum', 'x', '', '[{1..n}] BigNum'),
            ('x(): nil', 'x', '', 'nil'),
        ]
        for sig, name, arglist, retann in test_cases:
            self.check_sig(sig, None, None, name, arglist, retann)

    def test_with_class_names(self):
        """Verify function signatures with class names parse correctly."""
        test_cases = [
            ('X.x()', 'X.', 'x', ''),
            ('my.foo()', 'my.', 'foo', ''),
            ('1.1', '1.', '1', None),
            ('1.1()', '1.', '1', ''),
            ('BigNum.+(a, b)', 'BigNum.', '+', 'a, b'),
            ('BigNum.fromInt()', 'BigNum.', 'fromInt', ''),
            ('Vector.top', 'Vector.', 'top', None),
            ('MyMod.MyClass.foo()', 'MyMod.MyClass.', 'foo', ''),
        ]
        for sig, class_name, name, arglist in test_cases:
            self.check_sig(sig, None, class_name, name, arglist, None)


class AttrSigPatternTests(PatternTestCase):
    """Verify chpl_attr_sig_pattern regex."""

    pattern = chpl_attr_sig_pattern

    def check_sig(self, sig, func_prefix, name_prefix, name, retann):
        """Verify signature results in appropriate matches."""
        match = self.pattern.match(sig)
        self.assertIsNotNone(match)

        (actual_func_prefix, actual_name_prefix, actual_name, actual_retann) = match.groups()
        self.assertEqual(func_prefix, actual_func_prefix)
        self.assertEqual(name_prefix, actual_name_prefix)
        self.assertEqual(name, actual_name)
        self.assertEqual(retann, actual_retann)

    def test_does_not_match(self):
        """Verify various signatures that should not match."""
        test_cases = [
            '...',
            '.',
            '-',
            '----',
            ':::',
            '@',
            '#',
        ]
        for sig in test_cases:
            self.check_is_not_match(sig)

    def test_simple_label(self):
        """Verify various symbols match pattern."""
        test_cases = [
            'x',
            'myVar',
            'l_l',
            '123',
            '1',
        ]
        for sig in test_cases:
            self.check_sig(sig, '', None, sig, None)

    def test_with_class_names(self):
        """Verify symbols with class names match pattern."""
        test_cases = [
            ('my.var', 'my.', 'var'),
            ('1.1', '1.', '1'),
            ('BigNum.fromInt', 'BigNum.', 'fromInt'),
        ]
        for sig, class_name, attr in test_cases:
            self.check_sig(sig, '', class_name, attr, None)

    def test_with_prefixes(self):
        """Verify type, config, etc prefixes work."""
        test_cases = [
            ('type foo', 'type ', 'foo'),
            ('config const bar', 'config const ', 'bar'),
            ('config var x', 'config var ', 'x'),
            ('var y', 'var ', 'y'),
            ('const baz', 'const ', 'baz'),
        ]
        for sig, prefix, attr in test_cases:
            self.check_sig(sig, prefix, None, attr, None)

    def test_with_types(self):
        """Verify types parse correctly."""
        test_cases = [
            ('foo: int', 'foo', 'int'),
            ('bar: real', 'bar', 'real'),
            ('baz: int(32)', 'baz', 'int(32)'),
            ('D: domain(9)', 'D', 'domain(9)'),
            ('A: [{1..n}] BigNum', 'A', '[{1..n}] BigNum'),
            ('x: MyModule.MyClass', 'x', 'MyModule.MyClass'),
        ]
        for sig, attr, type_name in test_cases:
            self.check_sig(sig, '', None, attr, type_name)

    def test_with_all(self):
        """Verify full specified signatures parse correctly."""
        test_cases = [
            ('config const MyModule.MyClass.n: int', 'config const ', 'MyModule.MyClass.', 'n', 'int'),
            ('var X.n: MyMod.MyClass', 'var ', 'X.', 'n', 'MyMod.MyClass'),
            ('config param debugAdvancedIters:bool', 'config param ', None, 'debugAdvancedIters', 'bool'),
            ('config param MyMod.DEBUG: bool', 'config param ', 'MyMod.', 'DEBUG', 'bool'),
        ]
        for sig, prefix, class_name, attr, type_name in test_cases:
            self.check_sig(sig, prefix, class_name, attr, type_name)


if __name__ == '__main__':
    unittest.main()
