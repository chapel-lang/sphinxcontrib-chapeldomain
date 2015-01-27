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
    pip install -r requirements.txt -r test-requirements.txt
    ... develop ...
    tox

Testing
-------

Travis_ runs the tests automically and records code coverage in Coveralls_. On
a local workstation, tox_ can be used to run the tests in a similar fashion.

.. code-block:: bash

    tox              # run unittests with py27, py34
    tox -e flake8    # flake8 source code checker
    tox -e coverage  # run code coverage analysis
    tox -e docs      # verify the docs build
    tox -e doc-test  # verify the acceptance tests build

.. _Travis: https://travis-ci.org/chapel-lang/sphinxcontrib-chapeldomain
.. _Coveralls: https://coveralls.io/r/chapel-lang/sphinxcontrib-chapeldomain?branch=master
.. _tox: https://tox.readthedocs.org/en/latest/
