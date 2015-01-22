Classy?
=======

Let's hope so...

Chapel classes
--------------

#.. default-domain:: chpl

.. class:: ChplVector

    .. method:: ChplVector(type eltType, cap=4, offset=0)


Python classes
--------------


.. py:module:: PyContainers
    :synopsis: Container classes! Currently, just Vector.

.. py:class:: PyVector

    .. py:attribute:: eltType

        Generic type of Vector.

    .. py:attribute:: capacity

        Should be type ``int``.

    .. py:attribute:: lastIdx

        Should be type ``int``

    .. py:attribute:: dom

        Should be type ``domain(1)``

    .. py:attribute:: elements

        Should be of type ``[dom] eltType``

    .. py:method:: Vector(type eltType, cap=4, offset=0)

        Intialize new instance with given args.

        :arg type eltType: generic type for Vector elements
        :arg int cap: Capacity for vector.
        :arg int offset: Vector offset.

    .. py:method:: push(_mt: _MT, this: Vector, val: .(this, "eltType"))

    .. py:method:: low(_mt: _MT, this: Vector)

    .. py:method:: high(_mt: _MT, this: Vector)

    .. py:method:: pop(_mt: _MT, this: Vector)

    .. py:method:: top(_mt: _MT, this: Vector) ref

    .. py:method:: this(_mt: _MT, this: Vector, idx) ref

    .. py:method:: these(_mt: _MT, this: Vector) ref

    .. py:method:: size(_mt: _MT, this: Vector)

    .. py:method:: empty(_mt: _MT, this: Vector)
