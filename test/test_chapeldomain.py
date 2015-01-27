# -*- coding: utf-8 -*-

"""Verify sphinxcontrib.chapeldomain.ChapelDomain."""

from __future__ import print_function, unicode_literals

import mock
import unittest

from sphinxcontrib.chapeldomain import (
    ChapelDomain, ChapelObject,
    chpl_sig_pattern, chpl_attr_sig_pattern,
)


class ChapelDomainTests(unittest.TestCase):
    """ChapelDomain tests."""

    def test_init(self):
        """Simple test to verify ChapelDomain can be initialized."""
        env = mock.Mock()
        env.domaindata = {'name': 'chapel'}
        self.assertIsNotNone(ChapelDomain(env))


class ChapelObjectTests(unittest.TestCase):
    """ChapelObject tests."""

    def new_obj(self, objtype, **kwargs):
        """Return new mocked out ChapelObject"""
        default_args = {
            'name': 'my-chpl',
            'arguments': mock.Mock('arguments'),
            'options': mock.Mock('options'),
            'content': mock.Mock('content'),
            'lineno': mock.Mock('lineno'),
            'content_offset': mock.Mock('content_offset'),
            'block_text': mock.Mock('block_text'),
            'state': mock.Mock('state'),
            'state_machine': mock.Mock('state_machine'),
        }
        default_args.update(kwargs)
        o = ChapelObject(**default_args)
        o.objtype = objtype
        return o

    def test_init(self):
        """Verify ChapelObject can be initialized."""
        self.assertIsNotNone(self.new_obj('blah'))

    def test_is_attr_like__true(self):
        """Verify _is_attr_like return True for data and
        attribute directives.
        """
        for objtype in ('data', 'attribute', 'type'):
            self.assertTrue(self.new_obj(objtype)._is_attr_like())

    def test_is_attr_like__false(self):
        """Verify _is_attr_like return False for non-attr like directive."""
        bad_dirs = [
            'function',
            'iterfunction',
            'method',
            'itermethod',
            'class',
            'record',
            'module',
            'random',
            '',
        ]
        for objtype in bad_dirs:
            self.assertFalse(self.new_obj(objtype)._is_attr_like())

    def test_is_proc_like__true(self):
        """Verify _is_proc_like returns True for proc-like directives."""
        good_dirs = [
            'function',
            'iterfunction',
            'method',
            'itermethod',
        ]
        for objtype in good_dirs:
            self.assertTrue(self.new_obj(objtype)._is_proc_like())

    def test_is_proc_like__false(self):
        """Verify _is_proc_like returns False for proc-like directives."""
        bad_dirs = [
            'data',
            'attribute',
            'type',
            'class',
            'record',
            'module',
            'random',
            '',
        ]
        for objtype in bad_dirs:
            self.assertFalse(self.new_obj(objtype)._is_proc_like())

    def test_get_attr_like_prefix(self):
        """Verify _get_attr_like_prefix returns correct value for several
        attribute and data signatures.
        """
        test_cases = [
            ('', ''),
            ('foo', ''),
            ('type T', 'type '),
            ('var x', 'var '),
            ('config const n', 'config const '),
            ('blah blah blah blah blah', 'blah blah blah blah '),
        ]
        for objtype in ('attribute', 'data'):
            obj = self.new_obj(objtype)
            for sig, prefix in test_cases:
                actual_prefix = obj._get_attr_like_prefix(sig)
                self.assertEqual(prefix, actual_prefix)

    def test_get_attr_like_prefix__type(self):
        """Verify _get_attr_like_prefix return correct value for
        type signatures.
        """
        test_cases = [
            ('', ''),
            ('foo', 'type '),
            ('type T', 'type '),
            ('var x', 'var '),
            ('config const n', 'config const '),
            ('blah blah blah blah blah', 'blah blah blah blah '),
        ]
        obj = self.new_obj('type')
        for sig, prefix in test_cases:
            actual_prefix = obj._get_attr_like_prefix(sig)
            self.assertEqual(prefix, actual_prefix)

    def test_get_attr_like_prefix__bad_objtype(self):
        """Verify weird case where sig matches, but objtype is incorrect."""
        actual_prefix = self.new_obj('bogus')._get_attr_like_prefix('foo')
        self.assertEqual('', actual_prefix)

    def test_get_proc_like_prefix__proc(self):
        """Verify _get_proc_like_prefix return correct value for
        several signatures.
        """
        test_cases = [
            ('', ''),
            ('_', 'proc '),
            ('foo', 'proc '),
            ('foo()', 'proc '),
            ('proc foo', 'proc '),
            ('inline proc foo', 'inline proc '),
            ('proc foo() ref', 'proc '),
            ('iter foo() ref', 'iter '),
            ('inline iter foo(x, y): int(32)', 'inline iter '),
            ('proc proc proc proc proc proc', 'proc proc proc proc proc '),
        ]
        for objtype in ('function', 'method'):
            obj = self.new_obj(objtype)
            for sig, prefix in test_cases:
                actual_prefix = obj._get_proc_like_prefix(sig)
                self.assertEqual(prefix, actual_prefix)

    def test_get_proc_like_prefix__iter(self):
        """Verify _get_proc_like_prefix return correct value for
        several signatures.
        """
        test_cases = [
            ('', ''),
            ('_', 'iter '),
            ('foo', 'iter '),
            ('foo()', 'iter '),
            ('proc foo', 'proc '),
            ('inline proc foo', 'inline proc '),
            ('proc foo() ref', 'proc '),
            ('iter foo() ref', 'iter '),
            ('inline iter foo(x, y): int(32)', 'inline iter '),
            ('iter iter iter iter iter iter', 'iter iter iter iter iter '),
        ]
        for objtype in ('iterfunction', 'itermethod'):
            obj = self.new_obj(objtype)
            for sig, prefix in test_cases:
                actual_prefix = obj._get_proc_like_prefix(sig)
                self.assertEqual(prefix, actual_prefix)

    def test_get_proc_like_prefix__bad_objtype(self):
        """Verify weird case where sig matches, but objtype is incorrect."""
        actual_prefix = self.new_obj('bogus')._get_proc_like_prefix('foo')
        self.assertEqual('', actual_prefix)

    def test_get_sig_prefix__non_proc_non_attr(self):
        """Verify returns '' for non-attr, non-proc objtype."""
        obj = self.new_obj('bogus')
        self.assertEqual('', obj._get_sig_prefix('x'))

    def test_get_sig_prefix__proc_like(self):
        """Verify return proc prefix for proc-like objtype."""
        for objtype in ('function', 'iterfunction', 'method', 'itermethod'):
            obj = self.new_obj(objtype)
            self.assertEqual('inline proc ', obj._get_sig_prefix('inline proc x'))

    def test_get_sig_prefix__attr_like(self):
        """Verify returns attr prefix for attr-like objtype."""
        for objtype in ('attribute', 'data', 'type'):
            obj = self.new_obj(objtype)
            self.assertEqual('config const ', obj._get_sig_prefix('config const x'))


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
            ('x() ref', 'x', '', 'ref'),
            ('x() const', 'x', '', 'const'),
            ('x(ref x:int(32)) const', 'x', 'ref x:int(32)', 'const'),
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

    def test_with_prefixes(self):
        """Verify functions with prefixes parse correctly."""
        test_cases = [
            ('proc foo()', 'proc ', 'foo', ''),
            ('inline proc foo()', 'inline proc ', 'foo', ''),
            ('inline proc +()', 'inline proc ', '+', ''),
            ('inline iter basic()', 'inline iter ', 'basic', ''),
        ]
        for sig, prefix, name, arglist in test_cases:
            self.check_sig(sig, prefix, None, name, arglist, None)

    def test_with_all(self):
        """Verify fully specified signatures parse correctly."""
        test_cases = [
            ('proc foo() ref', 'proc ', None, 'foo', '', 'ref'),
            ('iter foo() ref', 'iter ', None, 'foo', '', 'ref'),
            ('inline proc Vector.pop() ref', 'inline proc ', 'Vector.', 'pop', '', 'ref'),
            ('inline proc range.first', 'inline proc ', 'range.', 'first', None, None),
            ('iter Math.fib(n: int(64)): GMP.BigInt', 'iter ', 'Math.', 'fib', 'n: int(64)', 'GMP.BigInt'),
            ('proc My.Mod.With.Deep.NameSpace.1.2.3.432.foo()', 'proc ', 'My.Mod.With.Deep.NameSpace.1.2.3.432.', 'foo', '', None),
            ('these() ref', None, None, 'these', '', 'ref'),
            ('size', None, None, 'size', None, None),
            ('proc Util.toVector(type eltType, cap=4, offset=0): Containers.Vector', 'proc ', 'Util.', 'toVector', 'type eltType, cap=4, offset=0', 'Containers.Vector'),
        ]
        for sig, prefix, class_name, name, arglist, retann in test_cases:
            self.check_sig(sig, prefix, class_name, name, arglist, retann)


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
