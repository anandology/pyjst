
# pyjst

Pyjst is a library to compile python templates to javascript.

It uses pyjs compiler from [pyjamas](http://pyjs.org) toolkit.

Currently it supports web.py templates. Support for Jinja2 is planned.

## How to use

* Install pyjs from pyjamas.

        $ git clone git://pyjs.org/git/pyjamas.git
        $ cd pyjamas/pyjs
        $ python setup.py develop
    
* build pyjst

        $ cd pyjst
        $ python setup.py develop
    
* build example

        $ cd pyjst/examples/helloworld
        $ make
    
* open index.html in your browser.


