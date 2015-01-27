Chapel Domain Reference
=======================

.. default-domain:: rst
.. highlight:: rst

The Chapel domain (named ``chpl``) provides the directives outlined in this
document.

The Chapel domain is strongly influenced by the `Python domain`_ that comes
with Sphinx. In addition, this documentation takes cues from the documentation
on Sphinx domain support, including Python domains.

.. _Python domain: http://sphinx-doc.org/domains.html#the-python-domain

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

Signatures of functions, methods, classes, records, iterators, etc can be given
like would be written in Chapel.

Default values for optional arguments can be given. Signatures can also include
their declarations, return types, and return intents. For example::

    .. function:: inline proc foo()

    .. iterfunction:: inline iter bar() ref

    .. function:: proc baz(ref x) const

    .. data:: config const n: int

    .. type:: type T: domain(3, int, true)

    .. attribute:: param MyMod.MyClass.communicative: bool = false

    .. itermethod:: iter MyMod.MyClass.these(): string

.. _info-field-lists:

Info field lists
----------------

Inside Chapel description directives, ReST field lists with these fields are
recognized and formatted nicely:

* ``param``, ``parameter``, ``arg``, ``argument``: Description of a parameter.
* ``type``: Type of a parameter. Creates a link if possible.
* ``returns``, ``return``: Description of the return value.
* ``rtype``: Return type. Creates a link if possible.
* ``yields``, ``yield``: Description of the yield value, often used for
  iterators.
* ``ytype``: Description of the yield value.

The field names must consist of one of these keywords and an argument, except
for ``returns``, ``rtype``, ``yields``, and ``ytype``, which do not need an
argument. See example::

    .. chpl:module:: GMP
        :synopsis: multiple precision integer library

    .. chpl:record:: BigNum

        multiple precision instances

        .. chpl:method:: proc add(a:BigNum, b:BigNum)

            Add two big ints, ``a`` and ``b``, and store the result in ``this``
            instance.

            :arg a: BigNum to be added
            :type a: BigNum

            :arg BigNum b: BigNum to be added

            :returns: nothing, result is stored in current instance

        .. chpl:itermethod:: iter these() ref

            Arbitrary iterator that returns individual digits of this instance.

            :ytype: reference
            :yields: reference to each individual digit of BigNum

The above will render like this:

.. chpl:module:: GMP
    :noindex:
    :synopsis: multiple precision integer library

.. chpl:record:: BigNum
    :noindex:

    multiple precision instances

    .. chpl:method:: proc add(a:BigNum, b:BigNum)
        :noindex:

        Add two big ints, ``a`` and ``b``, and store the result in ``this``
        instance.

        :arg a: BigNum to be added
        :type a: BigNum

        :arg BigNum b: BigNum to be added

        :returns: nothing, result is stored in current instance

    .. chpl:itermethod:: iter these() ref
        :noindex:

        Arbitrary iterator that returns individual digits of this instance.

        :ytype: reference
        :yields: reference to each individual digit of BigNum

Note that it is possible to combine the ``arg`` and ``type`` fields into a
single ``arg`` field, like ``:arg BigNum b:``. The same is true for ``param``
fields.

.. _chapel-roles:

Cross-referencing Chapel objects
--------------------------------

The following roles refer to objects in modules and are possibly hyperlinked if
a matching identifier is found:

.. role:: chpl:mod

    Reference a module; a dotted name may be used.

.. role:: chpl:func
          chpl:iter

    Reference a Chapel function or iterator; dotted names may be used. The role
    text needs not include trailing parentheses to enhance readability.

.. role:: chpl:data
          chpl:const
          chpl:var
          chpl:param
          chpl:type

    Reference a module-level variable, constant, compiler param, or type.

.. role:: chpl:class
          chpl:record

    Reference a class or record; a dotted name may be used.

.. role:: chpl:meth
          chpl:iter

    Reference a method or iterator of an object (class or record). The role
    text can include the type name and the method name. If it occurs within the
    description of a type, the type name can be omitted. A dotted name may be
    used.

.. role:: chpl:attr

    Reference a data attribute (const, var, param, generic type) of an object.

The name enclosed in this markup can include a module name and/or a class or
record name. For example, ``:chpl:func:`writeln``` could refer to a function
named ``writeln`` in the current module, or the built-in function of that
name. In contrast, ``:chpl:func:`Foo.writeln``` clearly refers to the
``writeln`` function in the ``Foo`` module.

Normally, names in these roles are search first without any further
qualification, then with the current module name prepended, then with the
current module and class name (if any) prepended. If you prefix the name with a
dot, this order is reserved. For example, in the documentation of the ``IO``
module, ``:chpl:func:`writeln``` always refers to the built-in function, while
``:chpl:func:`.writeln``` refers to ``IO.open``.

A similar heuristic is used to determine whether the name is an attribute of
the currently documented class.

Also, if the name is prefixed with a dot, and no exact match is found, the
target is taken as a suffix and all object names with that suffix are
searched. For example, ``:chpl:meth:`.channel.read``` references the
``IO.channel.read()`` function, even if the current module is not ``IO``. Since
this can get ambiguous, if there is more than one possible match, you will get
a warning from Sphinx.

Note that you can combine the ``~`` and ``.`` prefixes:
``:chpl:meth:`~.channel.read``` will reference the ``IO.channel.read()``
method, but the visible link caption will only be ``read()``.
