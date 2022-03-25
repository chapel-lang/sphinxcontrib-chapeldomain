Developer Documentation
=======================

This document describes the tools and practices used to develop the Chapel
domain.

Overview
--------

* Fork the `repo on github`_.
* Create a well named branch.
* Run testing.
* Submit pull request.
* Email or @mention the team in the comments.

.. _repo on github: https://github.com/chapel-lang/sphinxcontrib-chapeldomain

.. code-block:: bash

    git clone <url_for_fork>
    cd sphinxcontrib-chapeldomain/
    git checkout -b <branch_name>
    python3 -m pip install -r requirements.txt -r test-requirements.txt
    ... develop ...
    tox

Testing
-------

`Github Actions`_ runs the tests automatically and records code coverage in
Codecov_. On a local workstation, tox_ can be used to run the tests in a
similar fashion.

.. code-block:: bash

    tox              # run unittests with py310
    tox -e flake8    # flake8 source code checker
    tox -e coverage  # run code coverage analysis
    tox -e docs      # verify the docs build
    tox -e doc-test  # verify the acceptance tests build

.. _Github Actions: https://github.com/chapel-lang/sphinxcontrib-chapeldomain/actions/workflows/CI.yml
.. _Codecov: https://codecov.io/gh/chapel-lang/sphinxcontrib-chapeldomain
.. _tox: https://tox.readthedocs.org/en/latest/

Release
-------

When a new `release on Github`_ is created, a Github Action will automatically
upload it to PyPI_.

You can also upload a test release to test.pypi by manually triggering the
`upload action`_ on the main repository or your fork.

.. _PyPI: https://pypi.python.org/pypi/sphinxcontrib-chapeldomain
.. _release on Github: https://github.com/chapel-lang/sphinxcontrib-chapeldomain/releases/new
.. _upload action: https://github.com/chapel-lang/sphinxcontrib-chapeldomain/actions/workflows/python-publish.yml
