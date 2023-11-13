<h2>Get a korali version</h1>
<pre>
git clone --quiet --single-branch https://github.com/cselab/korali &&
    cd korali &&
    git checkout c70d8e32258b7e2b9ed977576997dfe946816419
</pre>

<h2>Make a wheel</h2>

<pre>
sudo apt-get install -qq libeigen3-dev libgsl-dev  python3-pybind11 ccache > /dev/null
git clone -q --depth 1 https://github.com/slitvinov/dcomex-framework.git
> dcomex-framework/korali/config.hpp
CC='ccache cc' CFLAGS=-I/usr/include/eigen3 python -m pip wheel --verbose dcomex-framework/korali
</pre>
