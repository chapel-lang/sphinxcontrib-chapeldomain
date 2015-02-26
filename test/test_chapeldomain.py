# -*- coding: utf-8 -*-

"""Verify sphinxcontrib.chapeldomain.ChapelDomain."""

from __future__ import print_function, unicode_literals

import mock
import sys
import unittest

# For python 2.6 and lower, use unittest2.
if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    import unittest2 as unittest

from sphinxcontrib.chapeldomain import (
    ChapelDomain, ChapelModuleIndex, ChapelModuleLevel, ChapelObject,
    chpl_sig_pattern, chpl_attr_sig_pattern,
)


class ChapelDomainTests(unittest.TestCase):
    """ChapelDomain tests."""

    def test_init(self):
        """Simple test to verify ChapelDomain can be initialized."""
        env = mock.Mock()
        env.domaindata = {'name': 'chapel'}
        self.assertIsNotNone(ChapelDomain(env))


class ChapelModuleIndexTests(unittest.TestCase):
    """ChapelModuleIndex tests."""

    @classmethod
    def setUpClass(cls):
        """Initalize sphinx locale stuff."""
        super(ChapelModuleIndexTests, cls).setUpClass()
        import sphinx.locale
        sphinx.locale.init([], 'en')

    def setUp(self):
        """Add some useful values to this instance."""
        self.modules = {
            # Regular sub-module.
            'foo.bar.baz': ('index', '', '', False),

            # Module with sub-modules and a synopsis.
            'foo': ('index', 'foo module synopsis -- it has two submodules', '', False),

            # Regular sub-module, should be sorted b/w foo and foo.bar.baz.
            'foo.bar': ('index', '', '', False),

            # Regular sub-module with similar name to Boo (test Boo vs foo.Boo
            # when common prefix is foo.).
            'foo.Boo': ('index', '', '', False),

            # Regular module.
            'zed': ('other_doc', '', '', False),

            # Deprecated module with platform and synopsis.
            'Zedd': ('other_doc', 'use zed', 'linux', True),

            # Regular module with platform.
            'Boo': ('halloween', '', 'Mac', False),

            # Oddly names module that will exactly match the ignore
            # pattern. Also, it will generate a parent that is not real.
            'odd.': ('index', '', '', False),
        }

    def new_index(self, ignores=None):
        """Helper to create and return new ChapelModuleIndex."""
        env = mock.Mock()
        env.domaindata = {'name': 'chapel'}
        env.config = {'chapeldomain_modindex_common_prefix': ignores or []}
        domain = ChapelDomain(env)
        index = ChapelModuleIndex(domain)
        index.domain.data['modules'] = self.modules
        return index

    def test_init(self):
        """Simple test to verify ChapelModuleIndex can be initialized."""
        self.assertIsNotNone(self.new_index())

    def test_generate(self):
        """Verify an arbitrary set of modules is returned in correct order."""
        index = self.new_index()
        expected_contents = [
            ('b', [
                ['Boo', 0, 'halloween', 'module-Boo', 'Mac', '', ''],
            ]),
            ('f', [
                ['foo', 1, 'index', 'module-foo', '', '', 'foo module synopsis -- it has two submodules'],
                ['foo.bar', 2, 'index', 'module-foo.bar', '', '', ''],
                ['foo.bar.baz', 2, 'index', 'module-foo.bar.baz', '', '', ''],
                ['foo.Boo', 2, 'index', 'module-foo.Boo', '', '', ''],
            ]),
            ('o', [
                ['odd', 1, '', '', '', '', ''],
                ['odd.', 2, 'index', 'module-odd.', '', '', ''],
            ]),
            ('z', [
                ['zed', 0, 'other_doc', 'module-zed', '', '', ''],
                ['Zedd', 0, 'other_doc', 'module-Zedd', 'linux', 'Deprecated', 'use zed'],
            ]),
        ]

        contents, collapse = index.generate()
        self.assertFalse(collapse)
        self.assertEqual(expected_contents, contents)

    def test_generate__docnames(self):
        """Verify generate() returns modules that are in docnames list."""
        index = self.new_index()
        expected_contents = [
            ('b', [
                ['Boo', 0, 'halloween', 'module-Boo', 'Mac', '', ''],
            ]),
            ('z', [
                ['zed', 0, 'other_doc', 'module-zed', '', '', ''],
                ['Zedd', 0, 'other_doc', 'module-Zedd', 'linux', 'Deprecated', 'use zed'],
            ]),
        ]

        contents, collapse = index.generate(docnames=['halloween', 'other_doc'])
        self.assertFalse(collapse)
        self.assertEqual(expected_contents, contents)

    def test_generate__ignore_common_prefix(self):
        """Verify behavior when chapeldomain_modindex_common_prefix is set in
        configuration.
        """
        index = self.new_index(ignores=['foo.', 'odd.'])
        expected_contents = [
            ('b', [
                ['Boo', 0, 'halloween', 'module-Boo', 'Mac', '', ''],
                ['foo.bar', 1, 'index', 'module-foo.bar', '', '', ''],
                ['foo.bar.baz', 2, 'index', 'module-foo.bar.baz', '', '', ''],
                ['foo.Boo', 0, 'index', 'module-foo.Boo', '', '', ''],
            ]),
            ('f', [
                ['foo', 0, 'index', 'module-foo', '', '', 'foo module synopsis -- it has two submodules'],
            ]),
            ('o', [
                ['odd', 1, '', '', '', '', ''],
                ['odd.', 2, 'index', 'module-odd.', '', '', ''],
            ]),
            ('z', [
                ['zed', 0, 'other_doc', 'module-zed', '', '', ''],
                ['Zedd', 0, 'other_doc', 'module-Zedd', 'linux', 'Deprecated', 'use zed'],
            ]),
        ]

        contents, collapse = index.generate()
        self.assertTrue(collapse)
        self.assertEqual(expected_contents, contents)


class ChapelObjectTestCase(unittest.TestCase):
    """Helper for ChapelObject related tests."""

    object_cls = ChapelObject

    @classmethod
    def setUpClass(cls):
        """Initalize sphinx locale stuff."""
        super(ChapelObjectTestCase, cls).setUpClass()
        import sphinx.locale
        sphinx.locale.init([], 'en')

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
        o = self.object_cls(**default_args)
        o.objtype = objtype
        return o


class ChapelModuleLevelTests(ChapelObjectTestCase):
    """ChapelModuleLevel tests."""

    object_cls = ChapelModuleLevel

    def test_get_index_text__function__no_mod(self):
        """Verify get_index_text() for function without module."""
        mod = self.new_obj('function')
        expected_text = 'myProc() (built-in procedure)'
        actual_text = mod.get_index_text(None, ('myProc',))
        self.assertEqual(expected_text, actual_text)

    def test_get_index_text__function__mod(self):
        """Verify get_index_text() for function with module."""
        mod = self.new_obj('function')
        expected_text = 'myProc() (in module MyMod)'
        actual_text = mod.get_index_text('MyMod', ('myProc',))
        self.assertEqual(expected_text, actual_text)

    def test_get_index_text__iter__no_mod(self):
        """Verify get_index_text() for function without module."""
        mod = self.new_obj('iterfunction')
        expected_text = 'myProc() (built-in iterator)'
        actual_text = mod.get_index_text(None, ('myProc',))
        self.assertEqual(expected_text, actual_text)

    def test_get_index_text__iter__mod(self):
        """Verify get_index_text() for function with module."""
        mod = self.new_obj('iterfunction')
        expected_text = 'myProc() (in module MyMod)'
        actual_text = mod.get_index_text('MyMod', ('myProc',))
        self.assertEqual(expected_text, actual_text)

    def test_get_index_text__data__no_mod(self):
        """Verify get_index_text() for data without module."""
        mod = self.new_obj('data')
        expected_text = 'myThing (built-in variable)'
        actual_text = mod.get_index_text(None, ('myThing',))
        self.assertEqual(expected_text, actual_text)

    def test_get_index_text__data__mod(self):
        """Verify get_index_text() for data with module."""
        mod = self.new_obj('data')
        expected_text = 'myThing (in module MyMod)'
        actual_text = mod.get_index_text('MyMod', ('myThing',))
        self.assertEqual(expected_text, actual_text)

    def test_get_index_text__type__no_mod(self):
        """Verify get_index_text() for type without module."""
        mod = self.new_obj('type')
        expected_text = 'myType (built-in type)'
        actual_text = mod.get_index_text(None, ('myType',))
        self.assertEqual(expected_text, actual_text)

    def test_get_index_text__type__mod(self):
        """Verify get_index_text() for type with module."""
        mod = self.new_obj('type')
        expected_text = 'myType (in module MyMod)'
        actual_text = mod.get_index_text('MyMod', ('myType',))
        self.assertEqual(expected_text, actual_text)

    def test_get_index_text__other(self):
        """Verify get_index_text() returns empty string for object types other than
        function, attribute, and type.
        """
        for objtype in ('other', 'attribute', 'class', 'module', 'method', 'itermethod'):
            mod = self.new_obj(objtype)
            self.assertEqual('', mod.get_index_text('MyMod', ('myThing',)))

    def test_chpl_type_name(self):
        """Verify chpl_type_name property for different objtypes."""
        test_cases = [
            ('function', 'procedure'),
            ('iterfunction', 'iterator'),
            ('type', 'type'),
            ('data', ''),
            ('method', ''),
            ('itermethod', ''),
        ]
        for objtype, expected_type in test_cases:
            mod = self.new_obj(objtype)
            self.assertEqual(expected_type, mod.chpl_type_name)

    def test_needs_arglist(self):
        """Verify needs_arglist()."""
        test_cases = [
            ('function', True),
            ('iterfunction', True),
            ('type', False),
            ('data', False),
            ('method', False),
            ('itermethod', False),
        ]
        for objtype, expected in test_cases:
            mod = self.new_obj(objtype)
            self.assertEqual(expected, mod.needs_arglist())


class ChapelObjectTests(ChapelObjectTestCase):
    """ChapelObject tests."""

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

    longMessage = True
    pattern = chpl_sig_pattern

    def check_sig(self, sig, func_prefix, name_prefix, name, arglist, retann):
        """Verify signature results in appropriate matches."""
        fail_msg = 'sig: {0}'.format(sig)

        match = self.pattern.match(sig)
        self.assertIsNotNone(match, msg=fail_msg)

        (actual_func_prefix, actual_name_prefix, actual_name, actual_arglist, actual_retann) = match.groups()
        self.assertEqual(func_prefix, actual_func_prefix, msg=fail_msg)
        self.assertEqual(name_prefix, actual_name_prefix, msg=fail_msg)
        self.assertEqual(name, actual_name, msg=fail_msg)
        self.assertEqual(arglist, actual_arglist, msg=fail_msg)
        self.assertEqual(retann, actual_retann, msg=fail_msg)

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
            ('x(): int', 'x', '', ': int'),
            ('x(): MyMod.MyClass', 'x', '', ': MyMod.MyClass'),
            ('x(): int(32)', 'x', '', ': int(32)'),
            ('x():int(32)', 'x', '', ':int(32)'),
            ('x(y:int(64)):int(32)', 'x', 'y:int(64)', ':int(32)'),
            ('x(y:int(64), d: domain(r=2, i=int, s=true)): [{1..5}] real', 'x', 'y:int(64), d: domain(r=2, i=int, s=true)', ': [{1..5}] real'),
            ('x(): domain(1)', 'x', '', ': domain(1)'),
            ('x(): [{1..n}] BigNum', 'x', '', ': [{1..n}] BigNum'),
            ('x(): nil', 'x', '', ': nil'),
            ('x() ref', 'x', '', ' ref'),
            ('x() const', 'x', '', ' const'),
            ('x(ref x:int(32)) const', 'x', 'ref x:int(32)', ' const'),
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
            ('proc foo() ref', 'proc ', None, 'foo', '', ' ref'),
            ('iter foo() ref', 'iter ', None, 'foo', '', ' ref'),
            ('inline proc Vector.pop() ref', 'inline proc ', 'Vector.', 'pop', '', ' ref'),
            ('inline proc range.first', 'inline proc ', 'range.', 'first', None, None),
            ('iter Math.fib(n: int(64)): GMP.BigInt', 'iter ', 'Math.', 'fib', 'n: int(64)', ': GMP.BigInt'),
            ('proc My.Mod.With.Deep.NameSpace.1.2.3.432.foo()', 'proc ', 'My.Mod.With.Deep.NameSpace.1.2.3.432.', 'foo', '', None),
            ('these() ref', None, None, 'these', '', ' ref'),
            ('size', None, None, 'size', None, None),
            ('proc Util.toVector(type eltType, cap=4, offset=0): Containers.Vector', 'proc ', 'Util.', 'toVector', 'type eltType, cap=4, offset=0', ': Containers.Vector'),
            ('proc MyClass$.lock$(combo$): sync bool', 'proc ', 'MyClass$.', 'lock$', 'combo$', ': sync bool'),
            ('proc MyClass$.lock$(combo$): sync myBool$', 'proc ', 'MyClass$.', 'lock$', 'combo$', ': sync myBool$'),
            ('proc MyRs(seed: int(64)): int(64)', 'proc ', None, 'MyRs', 'seed: int(64)', ': int(64)'),
            ('proc RandomStream(seed: int(64) = SeedGenerator.currentTime, param parSafe: bool = true)',
             'proc ', None, 'RandomStream', 'seed: int(64) = SeedGenerator.currentTime, param parSafe: bool = true', None),
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
            ('foo: int', 'foo', ': int'),
            ('bar: real', 'bar', ': real'),
            ('baz: int(32)', 'baz', ': int(32)'),
            ('D: domain(9)', 'D', ': domain(9)'),
            ('A: [{1..n}] BigNum', 'A', ': [{1..n}] BigNum'),
            ('x: MyModule.MyClass', 'x', ': MyModule.MyClass'),
            ('x  :  sync real', 'x', '  :  sync real'),
        ]
        for sig, attr, type_name in test_cases:
            self.check_sig(sig, '', None, attr, type_name)

    def test_with_all(self):
        """Verify full specified signatures parse correctly."""
        test_cases = [
            ('config const MyModule.MyClass.n: int', 'config const ', 'MyModule.MyClass.', 'n', ': int'),
            ('var X.n: MyMod.MyClass', 'var ', 'X.', 'n', ': MyMod.MyClass'),
            ('config param debugAdvancedIters:bool', 'config param ', None, 'debugAdvancedIters', ':bool'),
            ('config param MyMod.DEBUG: bool', 'config param ', 'MyMod.', 'DEBUG', ': bool'),
            ('var RandomStreamPrivate_lock$: _syncvar(bool)', 'var ', None, 'RandomStreamPrivate_lock$', ': _syncvar(bool)'),
            ('var RandomStreamPrivate_lock$: sync bool', 'var ', None, 'RandomStreamPrivate_lock$', ': sync bool'),
            ('const RS$.lock$: sync MyMod$.MyClass$.bool', 'const ', 'RS$.', 'lock$', ': sync MyMod$.MyClass$.bool'),
            ('type commDiagnostics = chpl_commDiagnostics', 'type ', None, 'commDiagnostics', ' = chpl_commDiagnostics'),
            ('type age = int(64)', 'type ', None, 'age', ' = int(64)'),
            ('type MyMod.BigAge=BigNum.BigInt', 'type ', 'MyMod.', 'BigAge', '=BigNum.BigInt'),
        ]
        for sig, prefix, class_name, attr, type_name in test_cases:
            self.check_sig(sig, prefix, class_name, attr, type_name)


if __name__ == '__main__':
    unittest.main()
