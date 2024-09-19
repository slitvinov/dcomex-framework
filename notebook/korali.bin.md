---
jupyter:
  jupytext:
    formats: ipynb,md
    main_language: python
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.4
  kernelspec:
    display_name: Python 3
    name: python3
---

<!-- #region id="26e75489" -->
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/slitvinov/dcomex-framework/blob/master/notebook/korali.bin.ipynb)
<!-- #endregion -->

```sh id="be661e06"
git clone -q --depth 1 https://github.com/slitvinov/dcomex-framework.git
```

```sh id="705c8f73"
apt-get -qq install -qq --no-install-recommends libgsl-dev libeigen3-dev python3-pybind11
```

```python id="IjyD8uUPTjyW"
%pip install -qqq --progress-bar off mpi4py
```

```sh id="277024ef"
cd dcomex-framework/korali
make install 'USER = 1' -j `nproc`
```

```sh id="KG4GhLrabd-J"
cd dcomex-framework/korali/examples/features/running.cxx
make
./run-tmcmc
```
