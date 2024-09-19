---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.4
  kernelspec:
    display_name: Python 3
    name: python3
---

<!-- #region id="638af8d0-01f1-44ca-bcd7-08dbf245f194" -->
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/slitvinov/dcomex-framework/blob/master/notebook/korali.bin.ipynb)
<!-- #endregion -->

```python
%%sh
git clone https://github.com/slitvinov/dcomex-framework.git
```

```python
%%sh
apt-get -qq install --no-install-recommends libgsl-dev
```

```python
%%sh
cd dcomex-framework/koral
make install -j `nproc --all` 'USER = 1'
```
