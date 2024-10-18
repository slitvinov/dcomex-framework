```
jupytext --set-formats ipynb,md korali.ipynb korali.bin.ipynb
jupytext --sync korali.ipynb korali.bin.ipynb
```

Unpack
```
tar zxf 3.tar.gz
```

Collage
```
python immuno.py
montage -geometry +0+0 -tile 8x immuno.*.png out.png
```
