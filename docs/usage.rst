=====
Usage
=====

As command line tool
====================

After installation of jinn, you have to configure jinn.

Configuration
-------------

Set the absolute path to the directory of your `setup.cfg` explicitly as
environment variable::

    $ export JINN_CONFIG_PATH=/Users/martin/projects/project

You have to have a `setup.cfg` in the root of your project with the
following basic settings:


.. code-block:: ini

    [jinn]
    pkg_name = jinn
    base_dir = jinn
    default_env = dev

    [jinn:docs]
    docs_dir = docs/
    build_dir = _build_dir
    port = 8080


If you want to use the ``jinn.tasks.django`` you only have to add the
`dotted module path` to the `tasks` key in the `jinn section` in
`setup.cfg`.

.. code-block:: ini

    [jinn]
    pkg_name = jinn
    base_dir = jinn
    default_env = dev
    tasks =
        jinn.tasks.django


Some modules need a corresponding `section` in `setup.cfg`. So
``django`` does. So you have to add this section, otherwise a error will
be thrown.

.. code-block:: ini

    [jinn:django]
    port = 8000


Run
---

You can see all basic tasks with::

    $ jinn --list


Or show the help and all basic tasks::

    $ jinn



The basic tasks of jinn are the tasks that are enabled by default. You
can see the help of a specific task with::

    $ jinn help test.run

And a run a jinn task with the following command::

    $ jinn test.run

Chain tasks as you know it from a Makefile::

    $ jinn docs.html docs.open


As a library
============

Write your own tasks add them to jinn configuration section under
the key tasks.

.. code-block:: ini

    [jinn]
    pkg_name = jinn
    base_dir = jinn
    default_env = dev
    tasks =
        jinn.tasks.django
        myfancyapp.task
