=============
Configuration
=============

Example setup.cfg
=================

Jinn comes with a lot of `task modules` you can enable all with the
following `setup.cfg` configuration.

.. code-block:: ini

    [jinn]
    pkg_name = jinn
    base_dir = jinn
    default_env = dev
    tasks =
        jinn.tasks.django
        jinn.tasks.db
        jinn.tasks.heroku
        jinn.tasks.packagecloud
        jinn.tasks.standardjs

    [jinn:db]
    database = jinn
    username = jinn

    [jinn:django]
    port = 8000

    [jinn:docs]
    docs_dir = docs/
    build_dir = _build_dir
    port = 8080

    [jinn:packagecloud]
    username = transcode
