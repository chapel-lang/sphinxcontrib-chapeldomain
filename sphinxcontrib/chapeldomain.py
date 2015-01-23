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

import re

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, ObjType
from sphinx.locale import l_, _
from sphinx.roles import XRefRole
from sphinx.util.compat import Directive
from sphinx.util.docfields import Field, GroupedField, TypedField
from sphinx.util.nodes import make_refnode


VERSION = '0.0.1'


chpl_sig_pattern = re.compile(
    r"""^ (inline\s+)?             # prefixes
          ([\w.]*\.)?              # class name(s)
          (\w+)  \s*               # function or method name
          (?:\((.*)\))?            # optional: arguments
          (?:\s* [:\s] \s* (.*))?  #   or return type or ref intent
          $""", re.VERBOSE)


# FIXME: This might be needed to support something other than the -> for return
#        annotations. (thomasvandoren, 2015-01-20)
#
# class chapel_desc_returns(addnodes.desc_returns):
#     """Node for a "returns" annotation."""
#     def astext(self):
#         return ' : ' + nodes.TextElement.astext(self)
# nodes._add_node_class_names([chapel_desc_returns.__name__])


class ChapelField(Field):
    pass


class ChapelTypedField(TypedField):
    pass


# FIXME: rename ChapelObject -> ChapelBase
class ChapelObject(ObjectDescription):
    """FIXME"""

    option_spec = {
        'noindex': directives.flag,
        'module': directives.unchanged,
        'annotation': directives.unchanged,
    }

    doc_field_types = [
        TypedField('parameter', label=l_('Parameters'),
                   names=('param', 'parameter', 'arg', 'argument'),
                   typerolename='obj', typenames=('paramtype', 'type'),
                   can_collapse=True),
        Field('returnvalue', label=l_('Returns'), has_arg=False,
              names=('returns', 'return')),
        Field('returntype', label=l_('Return type'), has_arg=False,
              names=('rtype',)),
    ]

    stopwords = set((
        'const', 'var',
    ))

    @staticmethod
    def _pseudo_parse_arglist(signode, arglist):
        """Parse list of comma separated arguments.

        Arguments can have optional types.
        """
        paramlist = addnodes.desc_parameterlist()
        stack = [paramlist]
        try:
            for argument in arglist.split(','):
                argument = argument.strip()
                ends_open = 0
                ends_close = 0
                while argument.startswith('['):
                    stack.append(addnodes.desc_optional())
                    stack[-2] += stack[-1]
                    argument = argument[1:].strip()
                while argument.startswith(']'):
                    stack.pop()
                    argument = argument[1:].strip()
                while argument.endswith(']') and not argument.endswith('[]'):
                    ends_close += 1
                    argument = argument[:-1].strip()
                while argument.endswith('['):
                    ends_open += 1
                    argument = argument[:-1].strip()
                if argument:
                    stack[-1] += addnodes.desc_parameter(argument, argument)
                while ends_open:
                    stack.append(addnodes.desc_optional())
                    stack[-2] += stack[-1]
                    ends_open -= 1
                while ends_close:
                    stack.pop()
                    ends_close -= 1
            if len(stack) != 1:
                raise IndexError
        except IndexError:
            # If there are too few or too many elements on the stack, just give
            # up and treat the whole argument list as one argument, discarding
            # the already partially populated paramlist node.
            signode += addnodes.desc_parameterlist()
            signode[-1] += addnodes.desc_parameter(arglist, arglist)
        else:
            signode += paramlist

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
        sig_match = chpl_sig_pattern.match(sig)
        if sig_match is None:
            raise ValueError('Signature does not parse: {0}'.format(sig))

        func_prefix, name_prefix, name, arglist, retann = sig_match.groups()

        modname = self.options.get(
            'module', self.env.temp_data.get('chpl:module'))
        classname = self.env.temp_data.get('chpl:class')

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
            signode += addnodes.desc_annotation(sig_prefix, sig_prefix)
        if func_prefix:
            signode += addnodes.desc_addname(func_prefix, func_prefix)
        if name_prefix:
            signode += addnodes.desc_addname(name_prefix, name_prefix)

        anno = self.options.get('annotation')

        signode += addnodes.desc_name(name, name)

        if not arglist:
            # If this needs and arglist, and parens were provided in the
            # signature, add a parameterlist. Chapel supports paren-less
            # functions and methods, which can act as computed properties. If
            # arglist is the empty string, the signature included parens. If
            # arglist is None, it did not include parens.
            if self.needs_arglist() and arglist is not None:
                # for callables, add an empty parameter list
                signode += addnodes.desc_parameterlist()
            if retann:
                signode += addnodes.desc_returns(retann, retann)  # FIXME: ? chapel_desc_returns(retann, retann)
            if anno:
                signode += addnodes.desc_annotation(' ' + anno, ' ' + anno)
            return fullname, name_prefix

        self._pseudo_parse_arglist(signode, arglist)
        if retann:
            signode += addnodes.desc_returns(retann, retann)  # FIXME: ? chapel_desc_returns(retann, retann)
        if anno:
            signode += addnodes.desc_annotation(' ' + anno, ' ' + anno)
        return fullname, name_prefix

    def get_index_text(self, modname, name):
        """Return the text for the index entry of the object."""
        raise NotImplementedError('must be implemented in subclasses')

    def add_target_and_index(self, name_cls, sig, signode):
        """FIXME"""
        modname = self.options.get(
            'module', self.env.temp_data.get('chpl:module'))
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
            self.env.temp_data.pop('chpl:class', None)


class ChapelTypeObject(ChapelObject):
    """FIXME"""


class ChapelClassMember(ChapelObject):
    """FIXME"""

    def needs_arglist(self):
        """FIXME"""
        return self.objtype == 'method'

    def get_index_text(self, modname, name_cls):
        """FIXME"""
        name, cls = name_cls
        add_modules = self.env.config.add_module_names
        if self.objtype == 'method':
            try:
                clsname, methname = name.rsplit('.', 1)
            except ValueError:
                if modname:
                    return _('%s() (in module %s)') % (name, modname)
                else:
                    return _('%s()') % name
            if modname and add_modules:
                return _('%s() (%s.%s method)') % (methname, modname, clsname)
            else:
                return _('%s() (%s method)') % (methname, clsname)
        elif self.objtype == 'attribute':
            try:
                clsname, attrname = name.rsplit('.', 1)
            except ValueError:
                if modname:
                    return _('%s (in module %s)') % (name, modname)
                else:
                    return name
            if modname and add_modules:
                return _('%s (%s.%s attribute)') % (attrname, modname, clsname)
            else:
                return _('%s (%s attribute)') % (attrname, clsname)
        else:
            return ''


class ChapelClassObject(ChapelObject):
    """FIXME"""

    def get_signature_prefix(self, sig):
        """FIXME"""
        return self.objtype + ' '

    def get_index_text(self, modname, name_cls):
        """FIXME"""
        if self.objtype in ('class', 'record'):
            if not modname:
                return _('%s (built-in %s)') % (name_cls[0], self.objtype)
            return _('%s (%s in %s)') % (name_cls[0], self.objtype, modname)
        else:
            return ''

    def before_content(self):
        """FIXME"""
        ChapelObject.before_content(self)
        if self.names:
            self.env.temp_data['chpl:class'] = self.names[0][0]
            self.clsname_set = True


class ChapelModuleLevel(ChapelObject):
    """FIXME"""

    def needs_arglist(self):
        """FIXME"""
        return self.objtype == 'function'

    def get_index_text(self, modname, name_cls):
        """FIXME"""
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
        'function': ObjType(l_('function'), 'func'),
        'class': ObjType(l_('class'), 'class'),
        'record': ObjType(l_('record'), 'record'),
        'method': ObjType(l_('method'), 'meth'),
        #'attribute': ObjType(l_('attribute'), 'attr'),
    }

    directives = {
        'const': ChapelModuleLevel,
        'var': ChapelModuleLevel,
        'function': ChapelModuleLevel,
        'class': ChapelClassObject,
        'record': ChapelClassObject,
        'method': ChapelClassMember,
        #'attribute': ChapelClassMember,
    }

    roles = {
        'const': ChapelXRefRole(),
        'var': ChapelXRefRole(),
        'func': ChapelXRefRole(),
        'class': ChapelXRefRole(),
        'record': ChapelXRefRole(),
        'meth': ChapelXRefRole(),
        #'attr': ChapelXRefRole(),
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
