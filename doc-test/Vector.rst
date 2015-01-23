.. generated with `chpldoc --docs-text-only modules/standard/Containers.chpl`
   and then modified to be rst

.. default-domain:: chpl

Module: Containers
==================

.. module:: Containers
    :synopsis: Container classes! Currently, just Vector

.. class:: Vector

    .. FIXME: should ~ links display as hole value or just leaf value??? (thomasvandoren, 2015-01-22)

    `FIXME: <only copyright comment in file>` blah blah
    :chpl:class:`~BitOps.clz`... :chpl:attr:`~MyModule.ChplVector.elements`
    blah blah :chpl:meth:`~MyModule.ChplBigNum.fromInt`. See :chpl:mod:`BitOps`.

    .. attribute:: eltType
    .. attribute:: capacity: int(64)
    .. attribute:: lastIdx: int(64)
    .. attribute:: dom: domain(1)
    .. attribute:: elements: [.(this, "dom")] .(this, "eltType")

    .. method:: Vector(type eltType, cap: _unknown, offset: _unknown)

    .. method:: push(val: .(this, "eltType"))

    .. method:: low

    .. method:: high

    .. method:: pop()

    .. method:: top ref

    .. method:: this(idx) ref

    .. FIXME: should we represent iterators as function/methods or give them a special directive? If we give them a special directive, how do we distinguish an iterator that is part of a class/record and a general iterators? For example, Vector.these() vs. fib(n). (thomasvandoren, 2015-01-22)

    #.. iterator:: these() ref

    .. method:: size

    .. method:: empty
