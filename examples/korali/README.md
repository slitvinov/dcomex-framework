
```
$ K=`python -m site --user-site`; mpicxx main.cpp -std=c++17 -I "$K"/korali `pkg-config --cflags --libs python3` -L "$K" -lkorali -lpython3.8 -Wl,-R"$K"
```

Python

```
$ mpiexec -n 3 --oversubscribe main.py
```

C++

```
$ mpiexec -n 3 --oversubscribe ./a.out
```
