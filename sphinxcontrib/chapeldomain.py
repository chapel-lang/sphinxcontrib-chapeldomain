# -*- coding: utf-8 -*-

"""
    sphinxcontrib.chapeldomain
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    The Chapel language domain.

    :copyright: Copyright 2014 by Chapel Team
    :license: Apache v2.0, see LICENSE for details.

    Chapel website: http://chapel.cray.com/
    Chapel spec:    http://chapel.cray.com/language.html

"""

from sphinx.directives import ObjectDescription
from sphinx.domains import Domain
from sphinx.roles import XRefRole
from sphinx.util.compat import Directive


class ChapelObject(ObjectDescription):
    """FIXME"""


class ChapelTypeObject(ChapelObject):
    """FIXME"""


class ChapelMemberObject(ChapelObject):
    """FIXME"""


class ChapelFunctionObject(ChapelObject):
    """FIXME"""


class ChapelClassObject(ChapelObject):
    """FIXME"""


class ChapelRecordObject(ChapelObject):
    """FIXME"""


class ChapelXRefRole(XRefRole):
    """FIXME"""


class ChapelNamespaceObject(Directive):
    """FIXME"""


class ChapelDomain(Domain):
    """FIXME"""

    name = 'chapel'
    labels = 'Chapel'

    object_types = {
        # FIXME:
    }

    directives = {
        # FIXME:
    }

    roles = {
        # FIXME:
    }

    initial_data = {
        # FIXME:
    }

    def clear_doc(self, docname):
        """FIXME"""

    def merge_domaindata(self, docnames, otherdata):
        """FIXME"""

    def resolve_xref(self, env, fromdocname, builder, typ, target,
                     node, contnode):
        """FIXME"""

    def resolve_any_xref(self, env, fromdocname, builder, target,
                         node, contnode):
        """FIXME"""

    def get_object(self):
        """FIXME"""
