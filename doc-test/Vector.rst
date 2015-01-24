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
    :chpl:func:`~BitOps.clz`... :chpl:attr:`~MyModule.ChplVector.elements`
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

    .. itermethod:: these() ref

        Iterate over elements in vector.

        :ytype: eltType
        :yields: Reference to element in vector.

    .. method:: size

    .. method:: empty
