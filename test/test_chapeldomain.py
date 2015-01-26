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
            '-',
            '---',
            ':::',
            '@',
            '#',
        ]
        for sig in test_cases:
            self.check_is_not_match(sig)


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


if __name__ == '__main__':
    unittest.main()
