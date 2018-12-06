planting operations
============================================

Machine.copy
------------------------------------------------

.. automodule:: planting.planting_module.operations.copy
    :members:
    :show-inheritance:

example.::

    node = Machine(ip='XXX', remote_user='XXX', password='XXX')
    node.copy(src='~/test.py', dest='~/copy/test.py')

Machine.create
--------------------------------------------------

.. automodule:: planting.planting_module.operations.create
    :members:
    :show-inheritance:

example.::

    node = Machine(ip='XXX', remote_user='XXX', password='XXX')
    node.create(path='~/test.py', state='file')
    node.create(path='~/test', state='dir')

Machine.download
----------------------------------------------------

.. automodule:: planting.planting_module.operations.download
    :members:
    :show-inheritance:

example.::

    node = Machine(ip='XXX', remote_user='XXX', password='XXX')
    node.download(url='XXX', dest='/tests/')

Machine.fetch
-------------------------------------------------

.. automodule:: planting.planting_module.operations.fetch
    :members:
    :show-inheritance:

example.::

    node = Machine(ip='XXX', remote_user='XXX', password='XXX')
    node.fetch(src='~/test.py', dest='~/test/)

Machine.jsoninfile
------------------------------------------------------

.. automodule:: planting.planting_module.operations.jsoninfile
    :members:
    :show-inheritance:

example-1.::

    node = Machine(ip='XXX', remote_user='XXX', password='XXX')
    # infile.conf: {"a": {"b": 1}}
    node.jsoninfile(path='/root/infile.conf', keys=["a","b"], val=1)

example-2.::

    node = Machine(ip='XXX', remote_user='XXX', password='XXX')
    # infile.conf: {"a": [{"b": 1}]}
    node.jsoninfile(path='/root/infile.conf', keys=["a",0,"b"], val=1)

Machine.move
------------------------------------------------

.. automodule:: planting.planting_module.operations.move
    :members:
    :show-inheritance:

example.::

    node = Machine(ip='XXX', remote_user='XXX', password='XXX')
    node.move(src='~/test.py', dest='~/move/)

Machine.pip
-----------------------------------------------

.. automodule:: planting.planting_module.operations.pip
    :members:
    :show-inheritance:

example.::

    node = Machine(ip='XXX', remote_user='XXX', password='XXX')
    node.pip(package='ansible', executable='pip-3.3')

Machine.remove
--------------------------------------------------

.. automodule:: planting.planting_module.operations.remove
    :members:
    :show-inheritance:

example.::

    node = Machine(ip='XXX', remote_user='XXX', password='XXX')
    node.move(src='~/test.py')

Machine.shell
-------------------------------------------------

.. automodule:: planting.planting_module.operations.shell
    :members:
    :show-inheritance:

example.::

    node = Machine(ip='XXX', remote_user='XXX', password='XXX')
    node.shell(command='cd ~/test')

Machine.unarchive
-----------------------------------------------------

.. automodule:: planting.planting_module.operations.unarchive
    :members:
    :show-inheritance:

example.::

    node = Machine(ip='XXX', remote_user='XXX', password='XXX')
    node.unarchiver(url='XXX', dest='/tests/')
