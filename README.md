# brummi

a cute ooc documentation generator

# installation

brummi is a Python program, you'll need Python 2.7 (not 3.x!) to run it. Also, for your own comfort, install [virtualenv](http://pypi.python.org/pypi/virtualenv/1.6.4).

Now, do that (assuming `python` is python 2.7):

    # create a virtualenv for your sick brummi experiments
    virtualenv dev
    # use it!
    . ./dev/bin/activate
    # now, pyooc is not part of the python package index yet, so install it manually.
    git clone git://github.com/fredreichbier/pyooc.git
    cd pyooc/
    python setup.py develop
    # finally, get brummi.
    git clone git://github.com/fredreichbier/brummi.git
    cd brummi/
    # this will install some dependencies
    python setup.py develop

# usage

first, create a ooc json repo for your code. in the future, brummi will do it for you, but for now, it doesn't:

    rock -backend=json -outpath=ooc_repo myfile.ooc

then, create a `config.json` for brummi. it's a text file containing json containing configuration options. see `example-config.json` for examples. `ooc_path` is the (relative or absolute) path to the json repo created above. `out_path` is the directory the resulting api docs will be put into.

then, run brummi:

    brummi config.json

and that's all for now. have fun -- and if you run into problems, ping me.
