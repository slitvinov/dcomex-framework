Running Multiple Experiments
=====================================================

In this tutorial we show how you can execute a series of experiments, in order to benefit from Korali's oversubscription capabilities.

Create a series of experiments:

.. code-block:: python

    for i in range(8):
      e = korali.Experiment()
      e["Problem"]["Type"] = "Evaluation/Bayesian/Inference/Reference"
      e["Problem"]["Likelihood Model"] = "Additive Normal"
      e["Problem"]["Reference Data"] = getReferenceData()
      e["Problem"]["Computational Model"] = lambda sampleData: model(sampleData, getReferencePoints())
      
      # Configuring CMA-ES parameters
      e["Solver"]["Type"] = "Optimizer/CMAES"
      ...

Set Experiment Vector
---------------------------
 
We can store experiments in a list `eList`:

.. code-block:: python

    # Adding Experiment to vector
    eList.append(e)

Run Experiment Vector
---------------------------

We can run all experiments in one Korali application

.. code-block:: python

    k.run(eList)

Running
---------------------------

We are now ready to run our example: `python3 ./run-cmaes`

Resuming Previous Run
---------------------------

Runs with multiple Korali experiments can also be resumed from a previous execution. For more information, see :ref:`Checkpoint / Resume <checkpoints>`. 

