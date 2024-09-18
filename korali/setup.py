from distutils.core import setup, Extension
import subprocess
import sys
import re
import os
try:
    ret = subprocess.run(("gsl-config", "--libs"),
                         capture_output=True, check=True,
                         timeout=100)
except (FileNotFoundError, subprocess.CalledProcessError) as e:
    sys.stderr.write("%s: error: %s\n" % (sys.argv[0], e))
    sys.exit(2)
if len(ret.stdout) < 2 or ret.stdout[0] != b"-" or ret.stdout[1] != b"L":
    i = ret.stdout.find(b" ")
    lib_dir = ret.stdout[2:i]
    libs = ret.stdout[i:]
else:
    sys.stderr.write("%s: error: wrong replay from gsl-config: %s\n" %
                     (sys.argv[0], ret.stdout))
    sys.exit(2)
lib_pathes = [
    os.path.join(lib_dir, b"lib" + e[2:] + b".a") for e in libs.split()
    if e[:2] == b"-l" and e != b"-lm"
]
for lib in lib_pathes:
    if not os.path.isfile(lib):
        sys.stdout.write("%s: error: no static library '%s'\n" %
                         (sys.argv[0], lib))
        sys.exit(2)
setup(ext_modules=[
    Extension(
        name="libkorali",
        include_dirs=["source", "."],
        extra_objects=[e.decode() for e in lib_pathes],
        sources=[
            "auxiliar/fs.cpp",
            "auxiliar/jsonInterface.cpp",
            "auxiliar/koraliJson.cpp",
            "auxiliar/kstring.cpp",
            "auxiliar/libco/libco.c",
            "auxiliar/logger.cpp",
            "auxiliar/math.cpp",
            "auxiliar/MPIUtils.cpp",
            "auxiliar/reactionParser.cpp",
            "auxiliar/rtnorm/rtnorm.cpp",
            "engine.cpp",
            "modules/conduit/concurrent/concurrent.cpp",
            "modules/conduit/conduit.cpp",
            "modules/conduit/distributed/distributed.cpp",
            "modules/conduit/sequential/sequential.cpp",
            "modules/distribution/distribution.cpp",
            "modules/distribution/multivariate/multivariate.cpp",
            "modules/distribution/multivariate/normal/normal.cpp",
            "modules/distribution/specific/multinomial/multinomial.cpp",
            "modules/distribution/specific/specific.cpp",
            "modules/distribution/univariate/beta/beta.cpp",
            "modules/distribution/univariate/cauchy/cauchy.cpp",
            "modules/distribution/univariate/exponential/exponential.cpp",
            "modules/distribution/univariate/gamma/gamma.cpp",
            "modules/distribution/univariate/geometric/geometric.cpp",
            "modules/distribution/univariate/igamma/igamma.cpp",
            "modules/distribution/univariate/laplace/laplace.cpp",
            "modules/distribution/univariate/logNormal/logNormal.cpp",
            "modules/distribution/univariate/normal/normal.cpp",
            "modules/distribution/univariate/poisson/poisson.cpp",
            "modules/distribution/univariate/truncatedNormal/truncatedNormal.cpp",
            "modules/distribution/univariate/uniformratio/uniformratio.cpp",
            "modules/distribution/univariate/uniform/uniform.cpp",
            "modules/distribution/univariate/univariate.cpp",
            "modules/distribution/univariate/weibull/weibull.cpp",
            "modules/experiment/experiment.cpp",
            "modules/module.cpp",
            "modules/neuralNetwork/layer/activation/activation.cpp",
            "modules/neuralNetwork/layer/convolution/convolution.cpp",
            "modules/neuralNetwork/layer/deconvolution/deconvolution.cpp",
            "modules/neuralNetwork/layer/input/input.cpp",
            "modules/neuralNetwork/layer/layer.cpp",
            "modules/neuralNetwork/layer/linear/linear.cpp",
            "modules/neuralNetwork/layer/output/output.cpp",
            "modules/neuralNetwork/layer/pooling/pooling.cpp",
            "modules/neuralNetwork/layer/recurrent/gru/gru.cpp",
            "modules/neuralNetwork/layer/recurrent/lstm/lstm.cpp",
            "modules/neuralNetwork/layer/recurrent/recurrent.cpp",
            "modules/neuralNetwork/neuralNetwork.cpp",
            "modules/problem/bayesian/bayesian.cpp",
            "modules/problem/bayesian/custom/custom.cpp",
            "modules/problem/bayesian/reference/reference.cpp",
            "modules/problem/design/design.cpp",
            "modules/problem/hierarchical/hierarchical.cpp",
            "modules/problem/hierarchical/psi/psi.cpp",
            "modules/problem/hierarchical/thetaNew/thetaNew.cpp",
            "modules/problem/hierarchical/theta/theta.cpp",
            "modules/problem/integration/integration.cpp",
            "modules/problem/optimization/optimization.cpp",
            "modules/problem/problem.cpp",
            "modules/problem/propagation/propagation.cpp",
            "modules/problem/reaction/reaction.cpp",
            "modules/problem/reinforcementLearning/continuous/continuous.cpp",
            "modules/problem/reinforcementLearning/discrete/discrete.cpp",
            "modules/problem/reinforcementLearning/reinforcementLearning.cpp",
            "modules/problem/sampling/sampling.cpp",
            "modules/problem/supervisedLearning/supervisedLearning.cpp",
            "modules/solver/agent/agent.cpp",
            "modules/solver/agent/continuous/continuous.cpp",
            "modules/solver/agent/continuous/VRACER/VRACER.cpp",
            "modules/solver/agent/discrete/discrete.cpp",
            "modules/solver/agent/discrete/dVRACER/dVRACER.cpp",
            "modules/solver/deepSupervisor/deepSupervisor.cpp",
            "modules/solver/deepSupervisor/optimizers/fAdaBelief/fAdaBelief.cpp",
            "modules/solver/deepSupervisor/optimizers/fAdaGrad/fAdaGrad.cpp",
            "modules/solver/deepSupervisor/optimizers/fAdam/fAdam.cpp",
            "modules/solver/deepSupervisor/optimizers/fGradientBasedOptimizer.cpp",
            "modules/solver/deepSupervisor/optimizers/fMadGrad/fMadGrad.cpp",
            "modules/solver/designer/designer.cpp",
            "modules/solver/executor/executor.cpp",
            "modules/solver/integrator/integrator.cpp",
            "modules/solver/integrator/montecarlo/MonteCarlo.cpp",
            "modules/solver/integrator/quadrature/Quadrature.cpp",
            "modules/solver/optimizer/AdaBelief/AdaBelief.cpp",
            "modules/solver/optimizer/Adam/Adam.cpp",
            "modules/solver/optimizer/CMAES/CMAES.cpp",
            "modules/solver/optimizer/DEA/DEA.cpp",
            "modules/solver/optimizer/gridSearch/gridSearch.cpp",
            "modules/solver/optimizer/MADGRAD/MADGRAD.cpp",
            "modules/solver/optimizer/MOCMAES/MOCMAES.cpp",
            "modules/solver/optimizer/optimizer.cpp",
            "modules/solver/optimizer/Rprop/Rprop.cpp",
            "modules/solver/sampler/HMC/HMC.cpp",
            "modules/solver/sampler/MCMC/MCMC.cpp",
            "modules/solver/sampler/Nested/Nested.cpp",
            "modules/solver/sampler/sampler.cpp",
            "modules/solver/sampler/TMCMC/TMCMC.cpp",
            "modules/solver/solver.cpp",
            "modules/solver/SSM/SSA/SSA.cpp",
            "modules/solver/SSM/SSM.cpp",
            "modules/solver/SSM/TauLeaping/TauLeaping.cpp",
            "sample/sample.cpp",
        ]),
])
