# -*- coding: utf-8 -*-

"""Verify sphinxcontrib.chapeldomain.ChapelDomain."""

from __future__ import print_function, unicode_literals

import docutils.nodes as nodes
import mock
import unittest

from sphinxcontrib.chapeldomain import (
    ChapelDomain, ChapelModuleIndex, ChapelClassObject, ChapelModuleLevel, ChapelObject,
    ChapelTypedField, ChapelClassMember,
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
    """ChapelClassObject tests."""

    object_cls = ChapelClassObject

    def test_get_index_test__enum__mod(self):
        """Verify get_index_test() for enum with module."""
        mod = self.new_obj('enum')
        expected_text = 'Color (enum in MyMod)'
        actual_text = mod.get_index_text('MyMod', ('Color',))
        self.assertEqual(expected_text, actual_text)

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
            ('opfunction', 'operator'),
            ('opmethod', ''),
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
            ('opfunction', True),
            ('opmethod', False),
        ]
        for objtype, expected in test_cases:
            mod = self.new_obj(objtype)
            self.assertEqual(expected, mod.needs_arglist())


class ChapelClassMemberTests(ChapelObjectTestCase):
    """ChapelClassMember tests."""
    object_cls = ChapelClassMember

    def test_init(self):
        self.assertIsNotNone(self.new_obj("neo"))

    def test_needs_arglist(self):
        """Verify needs_arglist()."""
        test_cases = [
            ('function', False),
            ('iterfunction', False),
            ('type', False),
            ('data', False),
            ('method', True),
            ('itermethod', True),
            ('opfunction', False),
            ('opmethod', True),
        ]
        for objtype, expected in test_cases:
            mod = self.new_obj(objtype)
            self.assertEqual(expected, mod.needs_arglist())

    def test_chpl_type_name(self):
        """Verify chpl_type_name property for different objtypes."""
        test_cases = [
            ('function', ''),
            ('iterfunction', ''),
            ('type', ''),
            ('data', ''),
            ('attribute', ''),
            ('method', 'method'),
            ('itermethod', 'iterator'),
            ('opfunction', ''),
            ('opmethod', 'operator'),
        ]
        for objtype, expected_type in test_cases:
            mod = self.new_obj(objtype)
            self.assertEqual(expected_type, mod.chpl_type_name)


class ChapelObjectTests(ChapelObjectTestCase):
    """ChapelObject tests."""

    def test_init(self):
        """Verify ChapelObject can be initialized."""
        self.assertIsNotNone(self.new_obj('blah'))

    def test_is_attr_like__true(self):
        """Verify _is_attr_like return True for data and
        attribute directives.
        """
        for objtype in ('data', 'attribute', 'type', 'enum','enumconstant'):
            self.assertTrue(self.new_obj(objtype)._is_attr_like())

    def test_needs_arglist(self):
        """Verify needs_arglist()."""
        test_cases = [
            ('function', False),
            ('iterfunction', False),
            ('type', False),
            ('data', False),
            ('method', False),
            ('itermethod', False),
            ('opfunction', False),
            ('opmethod', False),
        ]
        for objtype, expected in test_cases:
            mod = self.new_obj(objtype)
            self.assertEqual(expected, mod.needs_arglist())

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
            'opmethod',
            'opfunction',
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
            'opfunction',
            'opmethod',
        ]
        for objtype in good_dirs:
            self.assertTrue(self.new_obj(objtype)._is_proc_like())

    def test_is_proc_like__false(self):
        """Verify _is_proc_like returns False for non proc-like directives."""
        bad_dirs = [
            'data',
            'attribute',
            'type',
            'class',
            'record',
            'module',
            'random',
            'enum',
            'enumconstant',
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
            ('enum Color', 'enum '),
            ('enum constant USA', 'enum constant '),
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
            ('proc ref foo() ref', 'proc ref '),
            ('proc ref foo()', 'proc ref '),
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
            ('proc ref foo() ref', 'proc ref '),
            ('proc ref foo()', 'proc ref '),
            ('iter foo() ref', 'iter '),
            ('inline iter foo(x, y): int(32)', 'inline iter '),
            ('iter iter iter iter iter iter', 'iter iter iter iter iter '),
        ]
        for objtype in ('iterfunction', 'itermethod'):
            obj = self.new_obj(objtype)
            for sig, prefix in test_cases:
                actual_prefix = obj._get_proc_like_prefix(sig)
                self.assertEqual(prefix, actual_prefix)

    def test_get_proc_like_prefix__op(self):
        """Verify _get_proc_like_prefix return correct value for
        several operator signatures.
        """
        test_cases = [
            ('', ''),
            ('_', 'operator '),
            ('operator foo', 'operator '),
            ('operator foo()', 'operator '),
            ('operator foo', 'operator '),
            ('inline operator foo', 'inline operator '),
            ('operator foo() ref', 'operator '),
            ('operator foo() ref', 'operator '),
            ('inline operator foo(x, y): int(32)', 'inline operator '),
            ('operator operator operator operator operator operator',
             'operator operator operator operator operator '),
            ('operator +=(other:T)', 'operator '),
            ('operator --(other:T)', 'operator '),
        ]
        for objtype in ('opmethod', 'opfunction'):
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

    def test_get_sig_prefix__op_like(self):
        """Verify return proc prefix for operator objtype."""
        for objtype in ('opfunction', 'opmethod'):
            obj = self.new_obj(objtype)
            self.assertEqual('inline operator ',
                             obj._get_sig_prefix('inline operator +'))

    def test_get_sig_prefix__attr_like(self):
        """Verify returns attr prefix for attr-like objtype."""
        for objtype in ('attribute', 'data', 'type'):
            obj = self.new_obj(objtype)
            self.assertEqual('config const ', obj._get_sig_prefix('config const x'))


class ChapelTypedFieldTests(ChapelObjectTestCase):
    """Verify ChapelTypedField class."""

    def chpl_args(self, can_collapse=True):
        """Helper script to make a chapel-like argument field."""
        return ChapelTypedField(
            'parameter', label='Arguments',
            names=('param', 'parameter', 'arg', 'argument'),
            typerolename='chplref',
            typenames=('paramtype', 'type'),
            can_collapse=can_collapse
        )

    def test_init(self):
        """Verify ChapelTypedField can be initialized."""
        self.assertIsNotNone(self.chpl_args())

    def test_make_field__no_items(self):
        """Verify make_field() when items is empty."""
        result = self.chpl_args().make_field(mock.Mock(), mock.Mock(), [],
                                             env=mock.Mock())
        self.assertEqual('Arguments\n\n', result.astext())

    def test_make_field__one_items(self):
        """Verify make_field() when items has one element."""
        arg = self.chpl_args()
        result = arg.make_field(
            {'x': [nodes.Text('X_ARG_TYPE')]},
            'chpl',
            [('x', nodes.Text('x is a super important argument'))],
            env=mock.Mock()
        )
        self.assertEqual(
            'Arguments\n\nx : X_ARG_TYPE -- x is a super important argument',
            result.astext()
        )

    def test_make_field__one_items__no_collapse(self):
        """Verify make_field() when items has one element but is not
        collapsible.
        """
        arg = self.chpl_args(can_collapse=False)
        result = arg.make_field(
            {'x': [nodes.Text('X_ARG_TYPE')]},
            'chpl',
            [('x', nodes.Text('x is a super important argument'))],
            env=mock.Mock()
        )
        self.assertEqual(
            ('Arguments\n\n'
             'x : X_ARG_TYPE -- x is a super important argument'),
            result.astext()
        )
        # Assert that the one argument is in a list by crudely confirming a
        # bullet list was created.
        self.assertIn('<bullet_list>', str(result))

    def test_make_field__many_items(self):
        """Verify make_field() when items has more than one element."""
        arg = self.chpl_args(can_collapse=False)
        result = arg.make_field(
            {'x': [nodes.Text('X_ARG_TYPE')],
             'z': [nodes.Text('Z1'), nodes.Text('Z2'), nodes.Text('Z3')]},
            'chpl',
            [
                ('x', nodes.Text('x is a super important argument')),
                ('y', nodes.Text('y is less interesting')),
                ('z', nodes.Text('ZZZZ')),
            ],
            env=mock.Mock()
        )
        self.assertEqual(
            ('Arguments\n\n'
             'x : X_ARG_TYPE -- x is a super important argument\n\n'
             'y -- y is less interesting\n\n'
             'z : Z1Z2Z3 -- ZZZZ'),
            result.astext()
        )


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

    def check_sig(self, sig, func_prefix, name_prefix, name, arglist, retann, where_clause):
        """Verify signature results in appropriate matches."""
        fail_msg = 'sig: {0}'.format(sig)

        match = self.pattern.match(sig)
        self.assertIsNotNone(match, msg=fail_msg)

        (actual_func_prefix, actual_name_prefix, actual_name, actual_arglist, actual_retann, actual_where_clause) = match.groups()
        self.assertEqual(func_prefix, actual_func_prefix, msg=fail_msg)
        self.assertEqual(name_prefix, actual_name_prefix, msg=fail_msg)
        self.assertEqual(name, actual_name, msg=fail_msg)
        self.assertEqual(arglist, actual_arglist, msg=fail_msg)
        self.assertEqual(retann, actual_retann, msg=fail_msg)
        self.assertEqual(where_clause, actual_where_clause, msg=fail_msg)

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
            self.check_sig(sig, None, None, sig, None, None, None)

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
            self.check_sig(sig, None, None, name, '', None, None)

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
            self.check_sig(sig, None, None, name, arglist, None, None)

    def test_with_return_type(self):
        """Verify function signatures with return types parse correctly."""
        test_cases = [
            ('x(): int', 'x', '', ': int', None),
            ('x(): MyMod.MyClass', 'x', '', ': MyMod.MyClass', None),
            ('x(): int(32)', 'x', '', ': int(32)', None),
            ('x():int(32)', 'x', '', ':int(32)', None),
            ('x(y:int(64)):int(32)', 'x', 'y:int(64)', ':int(32)', None),
            ('x(y:int(64), d: domain(r=2, i=int, s=true)): [{1..5}] real', 'x', 'y:int(64), d: domain(r=2, i=int, s=true)', ': [{1..5}] real', None),
            ('x(): domain(1)', 'x', '', ': domain(1)', None),
            ('x(): [{1..n}] BigNum', 'x', '', ': [{1..n}] BigNum', None),
            ('x(): nil', 'x', '', ': nil', None),
            ('x() ref', 'x', '', ' ref', None),
            ('x() const', 'x', '', ' const', None),
            ('x(ref x:int(32)) const', 'x', 'ref x:int(32)', ' const', None),
        ]
        for sig, name, arglist, retann, where_clause in test_cases:
            self.check_sig(sig, None, None, name, arglist, retann, where_clause)

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
            self.check_sig(sig, None, class_name, name, arglist, None, None)

    def test_with_prefixes(self):
        """Verify functions with prefixes parse correctly."""
        test_cases = [
            ('proc foo()', 'proc ', 'foo', ''),
            ('inline proc foo()', 'inline proc ', 'foo', ''),
            ('inline operator +()', 'inline operator ', '+', ''),
            ('inline iter basic()', 'inline iter ', 'basic', ''),
            ('inline operator +', 'inline operator ', '+', None),
        ]
        for sig, prefix, name, arglist in test_cases:
            self.check_sig(sig, prefix, None, name, arglist, None, None)

    def test_with_where_clause(self):
        """Verify functions with where clauses parse correctly."""
        test_cases = [
            ('proc processArr(arr: [1..n] int, f: proc (int) int) where n > 0', 'proc ', 'processArr', 'arr: [1..n] int, f: proc (int) int', None, ' where n > 0'),
            ('proc processArr(arr: []) where arr.elemType == int', 'proc ', 'processArr', 'arr: []', None, ' where arr.elemType == int'),
            ('proc processDom(dom: domain) where dom.rank == 2', 'proc ', 'processDom', 'dom: domain', None, ' where dom.rank == 2'),
            ('proc processRec(r: MyRecord) where r.x > 0', 'proc ', 'processRec', 'r: MyRecord', None, ' where r.x > 0'),
            ('proc processRange(r: [1..n] int) where n > 0', 'proc ', 'processRange', 'r: [1..n] int', None, ' where n > 0'),
            ('proc processRange(r: range) where r.low > 1', 'proc ', 'processRange', 'r: range', None, ' where r.low > 1'),
            ('operator + (a: int, b: int) where a > 0', 'operator ', '+', 'a: int, b: int', None, ' where a > 0'),
        ]
        for sig, prefix, name, arglist, retann, where_clause in test_cases:
            self.check_sig(sig, prefix, None, name, arglist, retann, where_clause)

    def test_with_all(self):
        """Verify fully specified signatures parse correctly."""
        test_cases = [
            ('proc foo where a > b', 'proc ', None, 'foo', None, None, ' where a > b'), 
            ('proc foo() where a > b', 'proc ', None, 'foo', '', None, ' where a > b'), 
            ('proc foo:int where a > b', 'proc ', None, 'foo', None, ':int', ' where a > b'), 
            ('proc foo():int where a > b', 'proc ', None, 'foo', '', ':int', ' where a > b'), 
            ('proc foo ref where a > b', 'proc ', None, 'foo', None, ' ref', ' where a > b'), 
            ('proc foo() ref where a > b', 'proc ', None, 'foo', '', ' ref', ' where a > b'), 
            ('proc foo ref: int where a > b', 'proc ', None, 'foo', None, ' ref: int', ' where a > b'), 
            ('proc foo() ref: int where a > b', 'proc ', None, 'foo', '', ' ref: int', ' where a > b'),
            ('proc foo() ref', 'proc ', None, 'foo', '', ' ref', None),
            ('iter foo() ref', 'iter ', None, 'foo', '', ' ref', None),
            ('inline proc Vector.pop() ref', 'inline proc ', 'Vector.', 'pop', '', ' ref', None),
            ('inline proc range.first', 'inline proc ', 'range.', 'first', None, None, None),
            ('iter Math.fib(n: int(64)): GMP.BigInt', 'iter ', 'Math.', 'fib', 'n: int(64)', ': GMP.BigInt', None),
            ('proc My.Mod.With.Deep.NameSpace.1.2.3.432.foo()', 'proc ', 'My.Mod.With.Deep.NameSpace.1.2.3.432.', 'foo', '', None, None),
            ('these() ref', None, None, 'these', '', ' ref', None),
            ('size', None, None, 'size', None, None, None),
            ('proc Util.toVector(type eltType, cap=4, offset=0): Containers.Vector', 'proc ', 'Util.', 'toVector', 'type eltType, cap=4, offset=0', ': Containers.Vector', None),
            ('proc MyClass$.lock$(combo$): sync bool', 'proc ', 'MyClass$.', 'lock$', 'combo$', ': sync bool', None),
            ('proc MyClass$.lock$(combo$): sync myBool$', 'proc ', 'MyClass$.', 'lock$', 'combo$', ': sync myBool$', None),
            ('proc type currentTime(): int(64)', 'proc type ', None, 'currentTime', '', ': int(64)', None),
            ('proc param int.someNum(): int(64)', 'proc param ', 'int.', 'someNum', '', ': int(64)', None),
            ('proc MyRs(seed: int(64)): int(64)', 'proc ', None, 'MyRs', 'seed: int(64)', ': int(64)', None),
            ('proc RandomStream(seed: int(64) = SeedGenerator.currentTime, param parSafe: bool = true)',
             'proc ', None, 'RandomStream', 'seed: int(64) = SeedGenerator.currentTime, param parSafe: bool = true', None, None),
            ('class X', 'class ', None, 'X', None, None, None),
            ('class MyClass:YourClass', 'class ', None, 'MyClass', None, ':YourClass', None),
            ('class M.C : A, B, C', 'class ', 'M.', 'C', None, ': A, B, C', None),
            ('record R', 'record ', None, 'R', None, None, None),
            ('record MyRec:SuRec', 'record ', None, 'MyRec', None, ':SuRec', None),
            ('record N.R : X, Y, Z', 'record ', 'N.', 'R', None, ': X, Y, Z', None),
            ('proc rcRemote(replicatedVar: [?D] ?MYTYPE, remoteLoc: locale) ref: MYTYPE',
             'proc ', None, 'rcRemote', 'replicatedVar: [?D] ?MYTYPE, remoteLoc: locale', ' ref: MYTYPE', None),
            ('proc rcLocal(replicatedVar: [?D] ?MYTYPE) ref: MYTYPE',
             'proc ', None, 'rcLocal', 'replicatedVar: [?D] ?MYTYPE', ' ref: MYTYPE', None),
            ('proc specialArg(const ref x: int)', 'proc ', None, 'specialArg', 'const ref x: int', None, None),
            ('proc specialReturn() const ref', 'proc ', None, 'specialReturn', '', ' const ref', None),
            ('proc constRefArgAndReturn(const ref x: int) const ref', 'proc ', None, 'constRefArgAndReturn', 'const ref x: int', ' const ref', None),
            ('operator string.+(s0: string, s1: string) : string', 'operator ', 'string.', '+', 's0: string, s1: string', ' : string', None),
            ('operator *(s: string, n: integral) : string', 'operator ', None, '*', 's: string, n: integral', ' : string', None),
            ('inline operator string.==(param s0: string, param s1: string) param', 'inline operator ', 'string.', '==', 'param s0: string, param s1: string', ' param', None),
            ('operator bytes.=(ref lhs: bytes, rhs: bytes) : void ', 'operator ', 'bytes.', '=', 'ref lhs: bytes, rhs: bytes', ' : void ', None),
            # can't handle this pattern, ":" is set as punctuation, and casts don't seem to be doc'd anyway
            # ('operator :(x: bytes)', 'operator ', None, ':', 'x: bytes', None),
         ]
        for sig, prefix, class_name, name, arglist, retann, where_clause in test_cases:
            self.check_sig(sig, prefix, class_name, name, arglist, retann, where_clause)

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
            ('const x = false', 'const ', None, 'x', ' = false'),
            ('config const MyC.x: int(64) = 5', 'config const ', 'MyC.', 'x', ': int(64) = 5'),
            ('config param n: uint(64) = 5: uint(64)', 'config param ', None, 'n', ': uint(64) = 5: uint(64)'),
            ('var MyM.MyC.x = 4: uint(64)', 'var ', 'MyM.MyC.', 'x', ' = 4: uint(64)'),
            ('type MyT = 2*real(64)', 'type ', None, 'MyT', ' = 2*real(64)'),
            ('type myFloats = 2*(real(64))', 'type ', None, 'myFloats', ' = 2*(real(64))'),
            ('enum Color { Red, Yellow, Blue }', 'enum ', None, 'Color', ' { Red, Yellow, Blue }'),
            ('enum Month { January=1, February }', 'enum ', None, 'Month', ' { January=1, February }'),
            ('enum One { Neo }', 'enum ', None, 'One', ' { Neo }'),
            ('enum constant Pink', 'enum constant ', None, 'Pink', None),
            ('enum constant December', 'enum constant ', None, 'December', None),
            ('enum constant Hibiscus', 'enum constant ', None, 'Hibiscus', None),
            ('enum constant Aquarius', 'enum constant ', None, 'Aquarius', None)
        ]
        for sig, prefix, class_name, attr, type_name in test_cases:
            self.check_sig(sig, prefix, class_name, attr, type_name)


if __name__ == '__main__':
    unittest.main()
