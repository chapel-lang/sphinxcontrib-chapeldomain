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

from docutils import nodes

from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, ObjType
from sphinx.locale import l_
from sphinx.roles import XRefRole
from sphinx.util.compat import Directive
from sphinx.util.nodes import make_refnode


VERSION = '0.0.1'


class ChapelObject(ObjectDescription):
    """FIXME"""

    stopwords = set((
        'config', 'const', 'var',
    ))

    def _parse_type(self, node, chpl_type):
        """ """
        for part in [_f for _f in wsplit_re.split(chpl_type) if _f]:
            tnode = nodes.Text(part, part)
            if chpl_type not in self.stopwords:
                node += tnode


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


class ChapelModuleLevel(ChapelObject):
    """FIXME"""


class ChapelXRefRole(XRefRole):
    """FIXME"""

    def process_link(self, env, refnode, has_explicit_title, title, target):
        """FIXME"""
        if not has_explicit_title:
            title = title.lstrip('.')  ##
            target = target.lstrip('~')  ##
            if title[0:1] == '~':
                title = title[1:]
                colon = title.rfind('.')
                if colon != -1:
                    title = title[colon+1:]
        return title, target


class ChapelNamespaceObject(Directive):
    """FIXME"""


class ChapelDomain(Domain):
    """FIXME"""

    name = 'chpl'
    labels = 'Chapel'

    object_types = {
        'const': ObjType(l_('const'), 'const'),
        'var': ObjType(l_('var'), 'var'),
    }

    directives = {
        'const': ChapelModuleLevel,
        'var': ChapelModuleLevel,
    }

    roles = {
        'const': ChapelXRefRole(),
        'var': ChapelXRefRole(),
    }

    initial_data = {
        'functions': {},
        'modules': {},
        'objects': {},
    }

    def _find_obj(self, env, name, typ):
        """FIXME"""
        if not name:
            return None, None
        elif name in self.data['objects']:
            return name, self.data['objects'][name][0]
        else:
            return None, None

    def clear_doc(self, docname):
        """FIXME"""

    def merge_domaindata(self, docnames, otherdata):
        """FIXME"""

    def resolve_xref(self, env, fromdocname, builder, typ, target,
                     node, contnode):
        """FIXME"""
        import ipdb
        ipdb.set_trace()

        # target = 'constTest'
        # typ    = 'data'

        name, obj = self._find_obj(env, target, typ)
        if not obj:
            return None
        else:
            return make_refnode(builder, fromdocname, obj, name,
                                contnode, name)

    def resolve_any_xref(self, env, fromdocname, builder, target,
                         node, contnode):
        """FIXME"""

    def get_object(self):
        """FIXME"""


def setup(app):
    """Add Chapel domain to Sphinx app."""
    app.add_domain(ChapelDomain)
