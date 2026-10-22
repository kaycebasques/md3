Development
===========

.. toctree::
   :hidden:

   test

Setup
-----

Build the documentation:

.. code-block:: console

   ./bazelisk build //docs

Build and serve the documentation locally at ``http://0.0.0.0:8000``:

.. code-block:: console

   ./bazelisk run //:serve

Update Lockfiles
----------------

After modifying ``deps.in``, regenerate ``deps.txt``:

.. code-block:: console

   ./bazelisk run //:deps.update
