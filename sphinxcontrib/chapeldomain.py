# -*- coding: utf-8 -*-

"""
    sphinxcontrib.chapeldomain
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    The Chapel language domain.

    :copyright: Copyright 2015 by Chapel Team
    :license: Apache v2.0, see LICENSE for details.

    Chapel website: http://chapel.cray.com/
    Chapel spec:    http://chapel.cray.com/language.html

"""

from docutils import nodes

from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, ObjType
from sphinx.locale import l_, _
from sphinx.roles import XRefRole
from sphinx.util.compat import Directive
from sphinx.util.nodes import make_refnode


VERSION = '0.0.1'


class ChapelObject(ObjectDescription):
    """FIXME"""

    stopwords = set((
        'config', 'const', 'var',
    ))

    def get_signature_prefix(self, sig):
        """May return a prefix to put before the object name in the signature."""
        return ''

    def needs_arglist(self):
        """May return True if an empty argument list is to be generated even if the
        document contains none.
        """
        return False

    def handle_signature(self, sig, signode):
        """Transform a Chapel signature into RST nodes.

        FIXME
        """
        name_prefix, name, arglist, retann = None, sig, None, None
        modname = self.options.get(
            'module', None)  # self.env.ref_context.get('chpl:module'))
        classname = None  # self.env.ref_context.get('py:class')

        # import ipdb
        # ipdb.set_trace()
        
        if classname:
            add_module = False
            if name_prefix and name_prefix.startswith(classname):
                fullname = name_prefix + name
                # class name is given again in the signature
                name_prefix = name_prefix[len(classname):].lstrip('.')
            elif name_prefix:
                # class name is given in the signature, but different
                # (shouldn't happen)
                fullname = classname + '.' + name_prefix + name
            else:
                # class name is not given in the signature
                fullname = classname + '.' + name
        else:
            add_module = True
            if name_prefix:
                classname = name_prefix.rstrip('.')
                fullname = name_prefix + name
            else:
                classname = ''
                fullname = name

        signode['module'] = modname
        signode['class'] = classname
        signode['fullname'] = fullname

        sig_prefix = self.get_signature_prefix(sig)
        if sig_prefix:
            sig_node += addnodes.desc_annotation(sig_prefix, sig_prefix)

        if name_prefix:
            signode += addnodes.desc_addname(name_prefix, name_prefix)

        signode += addnodes.desc_name(name, name)

        # import ipdb
        # ipdb.set_trace()

        return fullname, name_prefix

    def get_index_text(self, modname, name):
        """Return the text for the index entry of the object."""
        raise NotImplementedError('must be implemented in subclasses')

    def add_target_and_index(self, name_cls, sig, signode):
        """FIXME"""
        modname = None
        # FIXME: is this module name stuff needed? (thomasvandoren, 2015-01-18)
        # modname = self.options.get(
        #     'module', self.env.ref_context.get('chpl:module'))
        fullname = (modname and modname + '.' or '') + name_cls[0]
        # note target
        if fullname not in self.state.document.ids:
            signode['names'].append(fullname)
            signode['ids'].append(fullname)
            signode['first'] = (not self.names)
            self.state.document.note_explicit_target(signode)
            objects = self.env.domaindata['chpl']['objects']
            if fullname in objects:
                self.state_machine.reporter.warning(
                    'duplicate object description of %s, ' % fullname +
                    'other instance in ' +
                    self.env.doc2path(objects[fullname][0]) +
                    ', use :noindex: for one of them',
                    line=self.lineno)
            objects[fullname] = (self.env.docname, self.objtype)

        indextext = self.get_index_text(modname, name_cls)
        if indextext:
            self.indexnode['entries'].append(('single', indextext,
                                              fullname, ''))

    def before_content(self):
        """FIXME: is this needed/correct?"""
        self.clsname_set = False

    def after_content(self):
        """FIXME: is this needed/correct?"""
        if self.clsname_set:
            self.env.ref_context.pop('chpl:class', None)

    def _parse_type(self, node, chpl_type):
        """FIXME"""
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

    def needs_arglist(self):
        return self.objtype == 'function'

    def get_index_text(self, modname, name_cls):
        if self.objtype == 'function':
            if not modname:
                return _('%s() (built-in function)') % name_cls[0]
            return _('%s() (in module %s)') % (name_cls[0], modname)
        elif self.objtype in ('const', 'var'):  # FIXME: no data for chapel
            if not modname:
                return _('%s (built-in variable)') % name_cls[0]
            return _('%s() (in module %s)') % (name_cls[0], modname)
        else:
            return ''
                


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
        'objects': {},  # FIXME? fullname -> docname, objtype
    }

    # def clear_doc(self, docname):
    #     """FIXME"""

    # def merge_domaindata(self, docnames, otherdata):
    #     """FIXME"""

    # def process_doc(self, env, docname, document):
    #     """FIXME"""

    def resolve_xref(self, env, fromdocname, builder,
                     type, target, node, contnode):
        """FIXME"""
        # import ipdb
        # ipdb.set_trace()
        
        if target not in self.data['objects']:
            return None
        obj = self.data['objects'][target]
        return make_refnode(builder, fromdocname, obj[0], target,
                            contnode, target)

        # modname = node.get('chpl:module')
        # clsname = node.get('chpl:class')
        # searchmode = node.hasattr('refspecific') and 1 or 0
        # matches = self.find_obj(env, modname, clsname, target,
        #                         type, searchmode)

        # if not matches:
        #     return None
        # elif len(matches) > 1:
        #     env.warn_node(
        #         'more than one target found for cross-reference '
        #         '%r: %s' % (target, ', '.join(match[0] for match in matches)),
        #         node)
        # name, obj = matches[0]

        # if obj[1] == 'module':
        #     3 / 0
        # else:
        #     4 / 0
        #     return make_refnode(builder, fromdocname, obj[0], name,
        #                         contnode, name)

    def resolve_any_xref(self, env, fromdocname, builder, target,
                         node, contnode):
        """FIXME"""
        modname = node.get('chpl:module')
        clsname = node.get('chpl:class')
        results = []

        # always search in "refspecific" mode with the :any: role
        matches = self.find_obj(env, modname, clsname, target, None, 1)
        for name, obj in matches:
            if obj[1] == 'module':
                1 / 0
            else:
                2 / 0
                results.append(('chpl:' + self.role_for_objtype(obj[1]),
                                make_refnode(builder, fromdocname, obj[0], name,
                                             contnode, name)))

        return results

    # def get_objects(self):
    #     """FIXME"""

    # def get_type_name(self, type, primary=False):
    #     """FIXME"""


def setup(app):
    """Add Chapel domain to Sphinx app."""
    app.add_domain(ChapelDomain)
