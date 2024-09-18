Multi-Agent Reinforcement Learning with VMAS: A Vectorized Multi-Agent Simulator for Collective Robot Learning
===============================================================================================================

The following examples are based on the `VMAS <https://arxiv.org/pdf/2207.03530.pdf>`_ python library. To install please run 

.. code-block:: bash
	   
	  pip install vmas

For a description of the MARL tasks and further information we refer to the `VMAS github <https://github.com/proroklab/VectorizedMultiAgentSimulator>`_.

Example
-------

For the vmas environments (navigation, balance, sampling) we follow the specifications of `TorchRL <https://arxiv.org/abs/2306.00577>`_ (3 agents, episode length 100).

The tasks can be selected with the :code:`--env` flag, e.g. to run the balance task

.. code-block:: bash
	   
	  python run-vracer.py --env balance
