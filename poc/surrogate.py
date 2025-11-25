from functools import partial
from jax import grad, vmap, jit
from jax.example_libraries import optimizers
from jax.nn import relu
from torch.utils import data
from tqdm import trange
import itertools
import jax
import jax.numpy as np
import math
import matplotlib.pyplot as plt
import numpy as onp
import scipy
import random


def MLP(layers, activation=relu):

    def init(rng_key):

        def init_layer(key, d_in, d_out):
            k1, k2 = jax.random.split(key)
            glorot_stddev = 1. / np.sqrt((d_in + d_out) / 2.)
            W = glorot_stddev * jax.random.normal(k1, (d_in, d_out))
            b = np.zeros(d_out)
            return W, b

        key, *keys = jax.random.split(rng_key, len(layers))
        params = list(map(init_layer, keys, layers[:-1], layers[1:]))
        return params

    def apply(params, inputs):
        for W, b in params[:-1]:
            outputs = np.dot(inputs, W) + b
            inputs = activation(outputs)
        W, b = params[-1]
        outputs = np.dot(inputs, W) + b
        return outputs

    return init, apply


class DataGenerator(data.Dataset):

    def __init__(self,
                 u,
                 y,
                 s,
                 batch_size=64,
                 rng_key=jax.random.PRNGKey(1234)):
        self.u = u
        self.y = y
        self.s = s
        self.N = u.shape[0]
        self.batch_size = batch_size
        self.key = rng_key

    def __getitem__(self, index):
        self.key, subkey = jax.random.split(self.key)
        inputs, outputs = self.__data_generation(subkey)
        return inputs, outputs

    @partial(jit, static_argnums=(0, ))
    def __data_generation(self, key):
        idx = jax.random.choice(key,
                                self.N, (self.batch_size, ),
                                replace=False)
        s = self.s[idx, :]
        y = self.y[idx, :]
        u = self.u[idx, :]
        inputs = (u, y)
        outputs = s
        return inputs, outputs


class DeepONet:

    def __init__(self, branch_layers, trunk_layers):
        self.branch_init, self.branch_apply = MLP(branch_layers,
                                                  activation=relu)
        self.trunk_init, self.trunk_apply = MLP(trunk_layers, activation=relu)
        branch_params = self.branch_init(rng_key=jax.random.PRNGKey(1234))
        trunk_params = self.trunk_init(rng_key=jax.random.PRNGKey(4321))
        params = (branch_params, trunk_params)
        self.opt_init, \
        self.opt_update, \
        self.get_params = optimizers.adam(optimizers.exponential_decay(1e-3,
                                                                      decay_steps=1000,
                                                                      decay_rate=0.95))
        self.opt_state = self.opt_init(params)
        self.itercount = itertools.count()
        self.loss_log = []

    def operator_net(self, params, u, y):
        branch_params, trunk_params = params
        B = self.branch_apply(branch_params, u)
        T = self.trunk_apply(trunk_params, y)
        outputs = np.sum(B * T)
        return outputs

    def residual_net(self, params, u, y):
        s_y = grad(self.operator_net, argnums=2)(params, u, y)
        return s_y

    def loss(self, params, batch):
        inputs, outputs = batch
        u, y = inputs
        pred = vmap(self.operator_net, (None, 0, 0))(params, u, y)
        loss = np.mean((outputs.flatten() - pred)**2)
        return loss

    @partial(jit, static_argnums=(0, ))
    def step(self, i, opt_state, batch):
        params = self.get_params(opt_state)
        g = grad(self.loss)(params, batch)
        return self.opt_update(i, g, opt_state)

    def train(self, dataset, nIter=10000):
        data = iter(dataset)
        pbar = trange(nIter)
        for it in pbar:
            batch = next(data)
            self.opt_state = self.step(next(self.itercount), self.opt_state,
                                       batch)
            if it % 100 == 0:
                params = self.get_params(self.opt_state)
                loss_value = self.loss(params, batch)
                self.loss_log.append(loss_value)
                pbar.set_postfix({'Loss': loss_value})

    @partial(jit, static_argnums=(0, ))
    def predict_s(self, params, U_star, Y_star):
        s_pred = vmap(self.operator_net, (None, 0, 0))(params, U_star, Y_star)
        return s_pred

    @partial(jit, static_argnums=(0, ))
    def predict_s_y(self, params, U_star, Y_star):
        s_y_pred = vmap(self.residual_net, (None, 0, 0))(params, U_star,
                                                         Y_star)
        return s_y_pred


tmpp = np.linspace(300, 1503, 1204)
int_arr = []
int_arr.append(int(0))
for x in tmpp:
    int_arr.append(int(x))
ind = np.array(int_arr)
u_all = np.load('params.npy')
y_all = np.load('time.npy')[:, ind]
s_all = np.load('volume.npy')[:, ind]
import numpy as onp

indices = onp.random.permutation(612)
training_idx, test_idx = indices[:510], indices[510:]
uut = u_all[training_idx]
yyt = y_all[training_idx]
sst = s_all[training_idx]
ss = np.delete(sst, np.argsort(sst[:, 1204])[-10:], axis=0)
uu = np.delete(uut, np.argsort(sst[:, 1204])[-10:], axis=0)
yy = np.delete(yyt, np.argsort(sst[:, 1204])[-10:], axis=0)
yyy = np.reshape(yy, (500 * 1205, 1)) / np.max(y_all)
sss = np.reshape(ss - np.min(s_all),
                 (500 * 1205, 1)) / (np.max(s_all) - np.min(s_all))
uuu1 = np.repeat(uu[:, :6], 1205, axis=0)
uuu2 = uuu1.at[:, 0].set((uuu1[:, 0] - np.min(u_all[:, 0])) /
                         (np.max(u_all[:, 0]) - np.min(u_all[:, 0])))
uuu3 = uuu2.at[:, 1].set((uuu1[:, 1] - np.min(u_all[:, 1])) /
                         (np.max(u_all[:, 1]) - np.min(u_all[:, 1])))
uuu4 = uuu3.at[:, 2].set((uuu1[:, 2] - np.min(u_all[:, 2])) /
                         (np.max(u_all[:, 2]) - np.min(u_all[:, 2])))
uuu5 = uuu4.at[:, 3].set((uuu1[:, 3] - np.min(u_all[:, 3])) /
                         (np.max(u_all[:, 3]) - np.min(u_all[:, 3])))
uuu6 = uuu5.at[:, 4].set((uuu1[:, 4] - np.min(u_all[:, 4])) /
                         (np.max(u_all[:, 4]) - np.min(u_all[:, 4])))
uuu = uuu6.at[:, 5].set((uuu1[:, 5] - np.min(u_all[:, 5])) /
                        (np.max(u_all[:, 5]) - np.min(u_all[:, 5])))
uuu.shape
m = 3
P_train = 1
key_train = jax.random.PRNGKey(0)
branch_layers = [6, 30, 50, 50, 500]
trunk_layers = [1, 10, 20, 500]
model = DeepONet(branch_layers, trunk_layers)
batch_size = 10000
dataset = DataGenerator(uuu, yyy, sss, batch_size)
model.train(dataset, nIter=40000)
from jax.flatten_util import ravel_pytree

_, param_fun = ravel_pytree(model.get_params(model.opt_state))
params = param_fun(np.load('Surrogate_params.npy'))
s_pred = model.predict_s(params, uuu, yyy)[:, None]
s_pred
Preds = s_pred * (np.max(s_all) - np.min(s_all)) + np.min(s_all)
Trus = sss * (np.max(s_all) - np.min(s_all)) + np.min(s_all)
np.sum(np.abs(Preds - Trus) / Trus) / s_pred.shape[0]
ytt = yyy
uuut = uuu
stt = sss
i = 52
plt.plot(ytt[1205 * i:1205 + 1205 * i] * np.max(y_all),
         s_pred[1205 * i:1205 + 1205 * i] * np.max(s_all),
         color='orange',
         label='Prediction')
plt.plot(ytt[1205 * i:1205 + 1205 * i] * np.max(y_all),
         stt[1205 * i:1205 + 1205 * i] * np.max(s_all),
         'b',
         alpha=0.4,
         label='Reference')
i = 168
plt.plot(ytt[1205 * i:1205 + 1205 * i] * np.max(y_all),
         s_pred[1205 * i:1205 + 1205 * i] * np.max(s_all),
         color='orange')
plt.plot(ytt[1205 * i:1205 + 1205 * i] * np.max(y_all),
         stt[1205 * i:1205 + 1205 * i] * np.max(s_all),
         'b',
         alpha=0.4)
i = 70
plt.plot(ytt[1205 * i:1205 + 1205 * i] * np.max(y_all),
         s_pred[1205 * i:1205 + 1205 * i] * np.max(s_all),
         color='orange')
plt.plot(ytt[1205 * i:1205 + 1205 * i] * np.max(y_all),
         stt[1205 * i:1205 + 1205 * i] * np.max(s_all),
         'b',
         alpha=0.4)
plt.xlabel('Time in days')
plt.ylabel('Tumor Volume in $m^3$')
plt.axis([0, 14, 0, 2.5e-7])
plt.legend()
plt.title('Surrogate-Predictions on Training Data')
plt.savefig('Training_Data.pdf')
utestrr = u_all[test_idx]
ytestrr = y_all[test_idx]
stestrr = s_all[test_idx]
stest = np.delete(stestrr, np.argsort(stestrr[:, 1204])[-10:], axis=0)
utest = np.delete(utestrr, np.argsort(stestrr[:, 1204])[-10:], axis=0)
ytest = np.delete(ytestrr, np.argsort(stestrr[:, 1204])[-10:], axis=0)
ytt = np.reshape(ytest, (92 * 1205, 1)) / np.max(y_all)
stt = np.reshape(stest - np.min(s_all),
                 (92 * 1205, 1)) / (np.max(s_all) - np.min(s_all))
uuu1t = np.repeat(utest[:, :6], 1205, axis=0)
uuu2t = uuu1t.at[:, 0].set((uuu1t[:, 0] - np.min(u_all[:, 0])) /
                           (np.max(u_all[:, 0]) - np.min(u_all[:, 0])))
uuu3t = uuu2t.at[:, 1].set((uuu1t[:, 1] - np.min(u_all[:, 1])) /
                           (np.max(u_all[:, 1]) - np.min(u_all[:, 1])))
uuu4t = uuu3t.at[:, 2].set((uuu1t[:, 2] - np.min(u_all[:, 2])) /
                           (np.max(u_all[:, 2]) - np.min(u_all[:, 2])))
uuu5t = uuu4t.at[:, 3].set((uuu1t[:, 3] - np.min(u_all[:, 3])) /
                           (np.max(u_all[:, 3]) - np.min(u_all[:, 3])))
uuu6t = uuu5t.at[:, 4].set((uuu1t[:, 4] - np.min(u_all[:, 4])) /
                           (np.max(u_all[:, 4]) - np.min(u_all[:, 4])))
uuut = uuu6t.at[:, 5].set((uuu1t[:, 5] - np.min(u_all[:, 5])) /
                          (np.max(u_all[:, 5]) - np.min(u_all[:, 5])))
params = model.get_params(model.opt_state)
params = param_fun(np.load('Surrogate_params.npy'))
s_pred = model.predict_s(params, uuut, ytt)[:, None]
i = 22
plt.plot(ytt[1205 * i:1205 + 1205 * i] * np.max(y_all),
         s_pred[1205 * i:1205 + 1205 * i] * np.max(s_all),
         color='orange',
         label='Prediction')
plt.plot(ytt[1205 * i:1205 + 1205 * i] * np.max(y_all),
         stt[1205 * i:1205 + 1205 * i] * np.max(s_all),
         'b',
         alpha=0.4,
         label='Reference')
i = 47
plt.plot(ytt[1205 * i:1205 + 1205 * i] * np.max(y_all),
         s_pred[1205 * i:1205 + 1205 * i] * np.max(s_all),
         color='orange')
plt.plot(ytt[1205 * i:1205 + 1205 * i] * np.max(y_all),
         stt[1205 * i:1205 + 1205 * i] * np.max(s_all),
         'b',
         alpha=0.4)
i = 74
plt.plot(ytt[1205 * i:1205 + 1205 * i] * np.max(y_all),
         s_pred[1205 * i:1205 + 1205 * i] * np.max(s_all),
         color='orange')
plt.plot(ytt[1205 * i:1205 + 1205 * i] * np.max(y_all),
         stt[1205 * i:1205 + 1205 * i] * np.max(s_all),
         'b',
         alpha=0.4)
plt.xlabel('Time in days')
plt.ylabel('Tumor Volume in $m^3$')
plt.legend()
plt.title('Surrogate-Predictions on Test Data')
plt.savefig('Test_Data.pdf')
Preds = s_pred * (np.max(s_all) - np.min(s_all)) + np.min(s_all)
Trus = stt * (np.max(s_all) - np.min(s_all)) + np.min(s_all)
np.sum(np.abs(Preds - Trus) / Trus) / s_pred.shape[0]
data_c = [
    375.1868, 573.5277, 669.3725, 762.1544, 976.2309, 239.851, 500.8968,
    718.6324, 905.4509, 1111.718, 321.9596, 469.5535, 738.2037, 950.2938,
    1091.091, 108.8538, 215.0905, 339.8851, 404.2003, 647.4177
]
data_c = [
    158.4588, 267.4446, 378.9722, 571.0281, 729.3532, 1089.811, 99.23126,
    242.1918, 409.5099, 773.3028, 1011.136, 1229.825, 117.0427, 206.9505,
    412.8519, 593.7879, 839.2525, 1064.408, 250.7445, 303.0367, 511.6464,
    640.2075, 1109.126, 1390.361
]
y_data = [
    0, 2, 4, 7, 9, 11, 0, 2, 4, 7, 9, 11, 0, 2, 4, 7, 9, 11, 0, 2, 4, 7, 9, 11
]
y_data = [0, 4, 6, 8, 11, 0, 4, 6, 8, 11, 0, 4, 6, 8, 11, 0, 4, 6, 8, 11]
len(data_c)
data = np.array(data_c)
y_data = np.array(y_data) / 14
data_scale = onp.zeros(20, )
(np.max(s_all) - np.min(s_all)) / np.min(s_all)
data_scale[:6] = (data[:6] - np.min(data[:6])) / np.min(data[:6])
data_scale[6:12] = (data[6:12] - np.min(data[6:12])) / np.min(data[6:12])
data_scale[12:18] = (data[12:18] - np.min(data[12:18])) / np.min(data[12:18])
data_scale[18:24] = (data[18:24] - np.min(data[18:24])) / np.min(data[18:24])
data_scale[:5] = (data[:5] - np.min(data[:5])) / np.min(data[:5])
data_scale[5:10] = (data[5:10] - np.min(data[5:10])) / np.min(data[5:10])
data_scale[10:15] = (data[10:15] - np.min(data[10:15])) / np.min(data[10:15])
data_scale[15:20] = (data[15:20] - np.min(data[15:20])) / np.min(data[15:20])
data_scale
np.max(s_all) - np.min(s_all)
(np.max(s_all) - np.min(s_all)) / np.min(s_all)
data_final = data_scale / (np.max(s_all) - np.min(s_all)) * np.min(s_all)
data_final
data_final * (np.max(s_all) -
              np.min(s_all)) / np.min(s_all) * np.min(data) + np.min(data)


def func(x):
    a, b, c, d, e, f = x
    for zz in zip(y_data, data_final):
        y, vol = zz
        sol = model.operator_net(params, np.array([a, b, c, d, e, f]), y)
        sigma = 0.001
        sq = np.sum(np.subtract(sol, vol)**2)
        ssq = sigma * sigma
        loss = loss - 0.5 * 1. * math.log(2 * math.pi * ssq) - 0.5 * sq / ssq
    return loss


lo = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
hi = 1.0, 1.0, 1.0, 1.0, 1.0, 1.0
samples = list(zip(*tmcmc(func, 15000, lo, hi, random=random.Random(1234))))
names = onp.array(["$\\mu$", "$k_{th}$", "$p_v$", "$S_v$", "$k_1$", "$L_p$"])
fig, axes = plt.subplots(nrows=6, ncols=6, figsize=(12, 12))
plt.rcParams['font.size'] = 13
plt.xticks(fontsize=18)
plt.yticks(fontsize=13)
for i in range(6):
    for j in range(6):
        if i != j:
            H, xe, ye = np.histogram2d(np.array(samples[i]),
                                       np.array(samples[j]),
                                       10,
                                       range=((lo[i], hi[i]), (lo[j], hi[j])),
                                       density=True)
            axes[i, j].set_aspect("equal", "box")
            axes[i, j].imshow(H.T,
                              interpolation="spline16",
                              origin="lower",
                              extent=(lo[i], hi[i], lo[j], hi[i]),
                              cmap=plt.get_cmap("jet"))
            axes[i, j].tick_params(axis='both', which='both', labelsize=8)
            axes[i, j].set_xlabel(names[i])
            axes[i, j].set_ylabel(names[j])
for i in range(6):
    axes[i, i].hist(np.array(samples[i]), density=True, stacked=True)
    axes[i, i].tick_params(axis='both', which='both', labelsize=8)
    axes[i, i].set_xlabel(names[i])
plt.tight_layout()
plt.show()
plt.savefig('All_params.pdf')
onp.mean(samples, axis=1)
samplers = np.array(samples)[:6, :]
samplers.shape
np.std(samplers, axis=1)
sigma_est = np.mean(np.array(samples)[6, :])
sigmass = np.array(samples)[6:, :]
means = onp.zeros(15)
stss1 = onp.zeros(15)
stss2 = onp.zeros(15)
for i in range(15):
    sol = onp.zeros((1000, ))
    for j in range(1000):
        sol[j] = onp.random.normal(
            model.operator_net(params, samplers[:, j], i / 14), 0.001)
    means[i] = np.mean(sol)
    stss1[i] = np.quantile(sol, 0.05)
    stss2[i] = np.quantile(sol, 0.95)
plt.plot(onp.linspace(0, 14, 15), means, label='Posterior Mean')
plt.plot(onp.linspace(0, 14, 15), stss2, label='Lower Quartil')
plt.plot(onp.linspace(0, 14, 15), stss1, label='Upper Quartil')
plt.plot(y_data * 14, data_final, 'x', label='Data')
plt.legend()
plt.xlabel('Time in Days')
plt.ylabel('Normalized Tumor Volume')
data = np.array(data_c)
data_t = data[5:10]
means_new = means * (np.max(s_all) - np.min(s_all)
                     ) / np.min(s_all) * np.min(data_t) + np.min(data_t)
means_new1 = stss1 * (np.max(s_all) - np.min(s_all)
                      ) / np.min(s_all) * np.min(data_t) + np.min(data_t)
means_new2 = stss2 * (np.max(s_all) - np.min(s_all)
                      ) / np.min(s_all) * np.min(data_t) + np.min(data_t)
plt.plot(onp.linspace(0, 14, 15), means_new, label='Posterior Mean')
plt.fill_between(onp.linspace(0, 14, 15),
                 means_new1,
                 means_new2,
                 color='b',
                 alpha=.1,
                 label='Predictive Uncertainty')
plt.plot(y_data[:5] * 14, data_t, 'x', label='Experimental Data')
plt.legend()
plt.xlabel('Time in Days')
plt.ylabel('Tumor Volume in mm^3')
plt.tight_layout()
plt.savefig('Tumor_data.pdf')


def tmcmc(fun,
          draws,
          lo,
          hi,
          beta=1,
          return_evidence=False,
          trace=False,
          random=None):

    def inside(x):
        for l, h, e in zip(lo, hi, x):
            if e < l or e > h:
                return False
        return True

    if scipy == None:
        raise ModuleNotFoundError("tmcm needs scipy")
    if np == None:
        raise ModuleNotFoundError("tmcm needs nump")
    uniform = random.uniform if random else Random.uniform
    betasq = beta * beta
    eps = 1e-6
    p = 0
    S = 0
    d = len(lo)
    x = [tuple(uniform(l, h) for l, h in zip(lo, hi)) for i in range(draws)]
    f = onp.fromiter((fun(x) for x in x), dtype=onp.dtype("float64"))
    x2 = [[None] * d for i in range(draws)]
    sigma = [[None] * d for i in range(d)]
    f2 = onp.empty_like(f)
    End = False
    Trace = []
    accept = draws
    while True:
        if trace:
            Trace.append((x[:], accept))
        if End == True:
            return Trace if trace else (x, S) if return_evidence else x
        old_p, plo, phi = p, p, 2
        while phi - plo > eps:
            p = (plo + phi) / 2
            temp = (p - old_p) * f
            M1 = scipy.special.logsumexp(temp) - math.log(draws)
            M2 = scipy.special.logsumexp(2 * temp) - math.log(draws)
            if M2 - 2 * M1 > math.log(2):
                phi = p
            else:
                plo = p
        if p > 1:
            p = 1
            End = True
        dp = p - old_p
        S += scipy.special.logsumexp(dp * f) - math.log(draws)
        weight = scipy.special.softmax(dp * f)
        mu = [kahansum(w * e[k] for w, e in zip(weight, x)) for k in range(d)]
        x0 = [[a - b for a, b in zip(e, mu)] for e in x]
        for l in range(d):
            for k in range(l, d):
                sigma[k][l] = sigma[l][k] = betasq * kahansum(
                    w * e[k] * e[l] for w, e in zip(weight, x0))
        ind = random.choices(range(draws),
                             cum_weights=list(kahancumsum(weight)),
                             k=draws)
        ind.sort()
        sqrtC = onp.real(scipy.linalg.sqrtm(sigma))
        accept = 0
        for i, j in enumerate(ind):
            delta = [random.gauss(0, 1) for k in range(d)]
            xp = tuple(a + b for a, b in zip(x[j], sqrtC @ delta))
            if inside(xp):
                fp = fun(xp)
                if fp > f[j] or p * fp > p * f[j] + math.log(uniform(0, 1)):
                    x[j] = xp[:]
                    f[j] = fp
                    accept += 1
            x2[i] = x[j][:]
            f2[i] = f[j]
        x2, x, f2, f = x, x2, f, f2


def kahancumvariance(a):
    n = 0
    s = 0.0
    s2 = 0.0
    for e in a:
        n += 1
        y = e - s
        s += y / n
        s2 += y * (e - s)
        yield s, s2 / n


def kahancummean(a):
    s = 0.0
    c = 0.0
    n = 0
    for e in a:
        y = e - c
        t = s + y
        c = (t - s) - y
        s = t
        n += 1
        yield s / n


def kahancumsum(a):
    s = 0.0
    c = 0.0
    for e in a:
        y = e - c
        t = s + y
        c = (t - s) - y
        s = t
        yield s


def kahansum(a):
    s = 0.0
    c = 0.0
    for e in a:
        y = e - c
        t = s + y
        c = (t - s) - y
        s = t
    return s


def mean(a):
    s = 0.0
    c = 0.0
    n = 0
    for e in a:
        y = e - c
        t = s + y
        c = (t - s) - y
        s = t
        n += 1
    return s / n
