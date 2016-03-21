=====
Usage
=====

As commandline tool
===================

After installation of jinn, you have to configure jinn.

Configuration
-------------

You have to have a `setup.cfg` in the root of your project with the
following settings::

```
[jinn]
pkg_name = jinn
base_dir = jinn
default_env = dev

[jinn:docs]
docs_dir = docs
build_dir = _build
port = 8080
```




Run
---

You can see all basic tasks with::

    jinn --list


Or you type only::

    jinn

to see the help and all basic tasks.


The basic tasks of jinn are the tasks that are enabled by default. You


show help of specific task::

    jinn help test.run


run jinn task::

    jinn test.run

As library
==========

::

    import jinn




write own tasks add them with in the jinn configuration section under
the key tasks::


tasks =
    jinn.tasks.django
    myfancyapp.task

