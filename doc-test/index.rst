.. Test Chapel Domain documentation master file, created by
   sphinx-quickstart on Tue Dec  9 21:54:48 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Test Chapel Domain!
===================

Chapel language
---------------

Module 'Foo'
~~~~~~~~~~~~

.. toctree::

   BitOps

.. default-domain:: chpl

.. const:: constTest

    This is a contant. Use :const:`constTest` for this and that.

.. var:: varTest

    This is some variable. Use :var:`varTest` for everyday needs. Otherwise,
    use :const:`constTest`...

CPP tests...
------------

.. cpp:class:: myclass

    My class here!

.. cpp:function:: module::myclass::operator std::vector<std::string>(myclass x, int y)

    Some function that does some c++ thing... See also :cpp:class:`myclass`.

.. cpp:function:: inline hello(std::string x)

    Inline hello world function...


Python tests...
---------------

.. py:data:: pyConstTest

    Stuff about the constant!

.. py:data:: pyVarTest

    Info about :py:data:`pyVarTest` and :py:const:`pyConstTest`...


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

