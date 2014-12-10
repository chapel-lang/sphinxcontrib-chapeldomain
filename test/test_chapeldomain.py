# -*- coding: utf-8 -*-

"""Verify sphinxcontrib.chapeldomain.ChapelDomain."""

from __future__ import print_function, unicode_literals

import mock
import unittest

from sphinxcontrib.chapeldomain import ChapelDomain


class ChapelDomainTests(unittest.TestCase):
    """ChapelDomain tests."""

    def test_init(self):
        """Simple test to verify ChapelDomain can be initialized."""
        env = mock.Mock()
        env.domaindata = {'name': 'chapel'}
        self.assertIsNotNone(ChapelDomain(env))


if __name__ == '__main__':
    unittest.main()
