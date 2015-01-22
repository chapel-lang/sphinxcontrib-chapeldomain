.. generated with `chpldoc --docs-text-only modules/standard/Containers.chpl`
   and then modified to be rst

Module: Containers
==================

.. #.. module:: Containers
.. #    :synopsis: Container classes! Currently, just Vector

.. Class: Vector
.. class:: Vector

    `FIXME: <only copyright comment in file>`

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

    #.. iterator:: these() ref

    .. method:: size

    .. method:: empty
