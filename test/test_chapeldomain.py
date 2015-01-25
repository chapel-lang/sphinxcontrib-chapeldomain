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

    pass


class SigPatternTests(PatternTestCase):
    """Verify chpl_sig_pattern regex."""

    def test_todo(self):
        self.fail('no')


class AttrSigPatternTests(PatternTestCase):
    """Verify chpl_attr_sig_pattern regex."""

    def test_does_not_match(self):
        """Verify various signatures that should not match."""
        sig = '...'
        match = chpl_attr_sig_pattern.match(sig)
        self.assertIsNone(match)

    def test_simple_label(self):
        """Verify various symbols match pattern."""
        sig = 'myVar'
        match = chpl_attr_sig_pattern.match(sig)
        self.assertIsNotNone(match)

        func_prefix, name_prefix, name, retann = match.groups()
        self.assertEqual('', func_prefix)
        self.assertEqual(None, name_prefix)
        self.assertEqual(sig, name)
        self.assertEqual(None, retann)


if __name__ == '__main__':
    unittest.main()
