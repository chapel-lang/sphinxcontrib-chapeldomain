Chapel Domain Reference
=======================

.. default-domain:: rst
.. highlight:: rst

The Chapel domain (named **chpl**) provides the directives outlined in this
document.

.. The Chapel domain is strongly influenced by the :ref:`Python domain
   <sphinx:domains>` that comes with Sphinx. The documentation also takes cues
   from the great documentation available on Sphinx domain support, including
   the Python domains.

Module Directives
-----------------

.. directive:: .. chpl:module:: name

    This directive marks the beginning of the description of a module. It does
    not create content (like e.g. :rst:dir:`chpl:class` does).

    This directive will also cause an entry in the global module index.

    The ``synopsis`` option should consist of one sentence describing the
    module's purpose. it is currently only used in the Global Module Index.

    The ``platform`` option, if present, is a comma-separated list of the
    platforms on which the module is available. If it is available on all
    platforms, the option should be omitted.

    The ``deprecated`` option can be given (with no value) to mark a module as
    deprecated. It will be designated as such in various locations then.

.. directive:: .. chpl:currentmodule:: name

    This directive tells Sphinx that the classes, functions, etc documented
    from here are in the given module (similar to :rst:dir:`chpl:module`), but
    it will not create index entries, an entry in the Global Module Index, or a
    link target for :rst:role:`chpl:mod`. This is helpful in situations where
    documentation for things in a module is spread over multiple files or
    sections. One location needs to have :rst:dir:`chpl:module` directive, and
    the others can have :rst:dir:`chpl:currentmodule`.

Module and Class Contents
-------------------------

The following directives are provided for module and class contents.

.. directive:: .. chpl:function:: name(parameters)

    Describes a module-level function. The signature should include the
    parameters as given in the Chapel definition. See :ref:`signatures` for
    details.

    For example::

        .. chpl:function:: factorial(x: int) : int

    For iterators, see :rst:dir:`chpl:iterfunction`. For methods and method
    iterators, see :rst:dir:`chpl:method` and :rst:dir:`chpl:itermethod`
    respectively.

    The description normally includes information about the parameters
    required, how they are used, side effects, return type, and return
    description.

    This information can (in any ``chpl`` directive) optionally be given in a
    structured form, see :ref:`info-field-lists`.

.. directive:: .. chpl:iterfunction:: name(parameters)

    Describes a module-level iterator. The description should be similar to
    :rst:dir:`chpl:function`.

.. directive:: .. chpl:data:: name

    Describes global data in a module including ``const``, ``var``, ``type``,
    ``param``, ``config const``, etc. Class, record, and instance attributes
    are not documented using this environment.

.. directive:: .. chpl:type:: name

    Describes global type in module. Generic types for classes and records are
    not documented using this environment (see :rst:dir:`chpl:attribute` for
    that).

.. directive:: .. chpl:class:: name
               .. chpl:class:: name(parameters)

    Describe a class. The signature can optionally include parentheses with
    parameters which will be shown as the constructor arguments. See also
    :ref:`signatures`.

    Methods and attributes belonging to the class should be placed in this
    directive's body. If they are placed outside, the supplied name should
    contain the class name so that cross-references still work.

    For example::

        .. chpl:class:: Foo

            .. chpl:method:: bar()

        or:

        .. chpl:class:: Bar
        .. chpl:method:: Bar.baz()

    The first way is the preferred one.

.. directive:: .. chpl:record:: name
               .. chpl:record:: name(parameters)

    Records work the same as :rst:dir:`chpl:class`.

.. directive:: .. chpl:attribute:: name

    Describes an object data attribute. This can be a ``param``, ``const``,
    ``var``, ``type``, etc. The description should include information about
    the type of the data to be expected and whether it may be changed directly.

.. directive:: .. chpl:method:: name(parameters)

    Describes an object instance method (for :rst:dir:`chpl:class` or
    :rst:dir:`chpl:record`). The description should include similar information
    to that described for :rst:dir:`chpl:function`. See also :ref:`signatures`
    and :ref:`info-field-lists`.

.. directive:: .. chpl:itermethod:: name(paramaters)

    Describes an object instance iterator method (for :rst:dir:`chpl:class` or
    :rst:dir:`chpl:record`). The description should be similar to
    :rst:dir:`chpl:iterfunction`.

.. _signatures:

Chapel Signatures
-----------------

.. FIXME: do it

.. _info-field-lists:

Info field lists
----------------

.. FIXME: do it

.. _chapel-roles:

Cross-referencing Chapel objects
--------------------------------

.. FIXME: do it

