planting network
=========================================

Machine.process
------------------------------------------------

.. automodule:: planting.planting_module.network.process
    :members:
    :show-inheritance:

example.::

    node = Machine(ip='XXX', ssh_user='XXX', ssh_pass='XXX')
    node.process(process='nginx', state='started')

Machine.wait\_for
--------------------------------------------------

.. automodule:: planting.planting_module.network.wait_for
    :members:
    :show-inheritance:

example.::

    node = Machine(ip='XXX', ssh_user='XXX', ssh_pass='XXX')
    node.wait_for(port='22', state='started', timeout=10)

