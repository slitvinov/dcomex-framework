```
python3 -m pip install openpyxl
```


```
jupytext --set-formats ipynb,md korali.ipynb korali.bin.ipynb
jupytext --sync korali.ipynb korali.bin.ipynb
```

Unpack
```
tar zxf 1.tar.gz
```

or

```
tar zxf 4.tar.gz
```

Collage
```
python immuno.py
montage -geometry +0+0 -tile 8x immuno.*.png out.png
```

```
each data sheet is a different cancer type, each column is a different
specimen. Msolve simulation initialization (time = 0) refers to day 10
of the experiment for 4T1 and B16F10 and for day 4 for MCA205. Also
for day 7 for B16F10 is time=0 for MSolve but we havent ran this yet
because it has anosotherapy in 7-9-11 in Msolve days (it is analysis
Set 2). "Control" columns correspond to the noImmunotherapy
ones. (analysis set 3). We can use only the "apdl..." columns and not
the "tranilast" because we havent model it. The volums in Excel are in
mm^3 the volumes in Msolve are in m^3 and they should be multiplied by
8 to account for the fact that we model only the 1/8 of the tumor'
```
