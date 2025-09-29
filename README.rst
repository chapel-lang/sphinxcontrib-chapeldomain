Chapel Domain for Sphinx
========================

Chapel_ domain for Sphinx_.

.. _Chapel: http://chapel-lang.org/
.. _Sphinx: http://sphinx-doc.org/

.. image:: https://github.com/chapel-lang/sphinxcontrib-chapeldomain/actions/workflows/CI.yml/badge.svg
    :target: https://github.com/chapel-lang/sphinxcontrib-chapeldomain/actions/workflows/CI.yml

.. image:: https://codecov.io/gh/chapel-lang/sphinxcontrib-chapeldomain/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/chapel-lang/sphinxcontrib-chapeldomain

`Package documentation`_ is available on readthedocs.org.

.. _Package documentation: //sphinxcontrib-chapeldomain.readthedocs.org/

Installation
------------

To install::

    python3 -m pip install sphinxcontrib-chapeldomain

To install from source on github_::

    git clone https://github.com/chapel-lang/sphinxcontrib-chapeldomain
    cd sphinxcontrib-chapeldomain
    python setup.py install

.. _github: https://github.com/chapel-lang/sphinxcontrib-chapeldomain

Making Changes
--------------

#. Test and commit changes
#. Merge your changes
#. Generate a new PyPI release

Making a Release
----------------

#. Go to main page for repo
#. Click “Releases” on right side of screen
#. Click “Draft a new release” button on top of screen
#. For the tag, make a new tag with the new version number
#. You can generate the release notes via the “generate release notes” button,
   comparing against the most recent release.  This will autofill in the details
   for you
#. Click “Publish release”
    - This will trigger the workflow to push a new release to PyPI, assuming no
      problems have snuck into our release procedure since the last time it was
      run
#. Open a PR bumping the version to the next version number so that we’re ready
   for the next change.  This should always be the first PR in a new release
   (otherwise we’ll have build issues), so it should be straight-forward to
   figure out how to do this

In case of issues, the release pushing job is in
.github/workflows/python-publish.yml

You can modify it to try and get things to work. If the issue has something to
do with what was pushed to PyPI, you can adjust it to send to
https://test.pypi.org/ instead and download from there. You’ll want to remove
the bad version from PyPI in that case, which will require access to a user
account associated with the repository on PyPI.

Getting Started
---------------

This is an example that covers several features of the Chapel domain::

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
