import compiler
from cStringIO import StringIO
import os.path
import sys

from pyjs.translator_proto import Translator

    
def pyjs_translate(source, filename):
    """Translates python source code into javascript using pyjs translator.
    """
    ast = compiler.parse(source)
    module_name, extension = os.path.splitext(os.path.basename(filename))
    
    output = StringIO()
    t = Translator(compiler, module_name, filename, source, ast, output)
    return output.getvalue()
    
def compile_webpy_template(source, filename):
    """Compiles a web.py template.
    """
    from web.template import Template
    text = Template.normalize_text(source)
    python_source = Template.generate_code(source, filename)
    python_source = "from webpy_ext import escape_, TemplateResult, ForLoop\n" + python_source
    return pyjs_translate(python_source, filename)
    
def compile_template(engine, source, filename):
    if engine == 'webpy':
        return compile_webpy_template(source, filename)
    elif engine == 'python':
        return pyjs_translate(source, filename)
    else:
        print >> sys.stderr, "Unknown engine: %r" % engine


PYJS_BOOTSTRAP = """
var $wnd = window;
var $doc = window.document;
var $pyjs = new Object();
var $p = null;
$pyjs.platform = 'safari';
$pyjs.global_namespace = this;
$pyjs.__modules__ = {};
$pyjs.modules_hash = {};
$pyjs.loaded_modules = {};
$pyjs.options = new Object();
$pyjs.options.arg_ignore = true;
$pyjs.options.arg_count = true;
$pyjs.options.arg_is_instance = true;
$pyjs.options.arg_instance_type = false;
$pyjs.options.arg_kwarg_dup = true;
$pyjs.options.arg_kwarg_unexpected_keyword = true;
$pyjs.options.arg_kwarg_multiple_values = true;
$pyjs.options.dynamic_loading = false;
$pyjs.trackstack = [];
$pyjs.track = {module:'__main__', lineno: 1};
$pyjs.trackstack.push($pyjs.track);
$pyjs.__active_exception_stack__ = null;
$pyjs.__last_exception_stack__ = null;
$pyjs.__last_exception__ = null;
$pyjs.in_try_except = 0;

/* start module: dynamic */
$pyjs.loaded_modules['dynamic'] = function (__mod_name__) {
	if($pyjs.loaded_modules['dynamic'].__was_initialized__) return $pyjs.loaded_modules['dynamic'];
	var $m = $pyjs.loaded_modules["dynamic"];
	$m.__repr__ = function() { return "<module: dynamic>"; };
	$m.__was_initialized__ = true;
	if ((__mod_name__ === null) || (typeof __mod_name__ == 'undefined')) __mod_name__ = 'dynamic';
	$m.__name__ = __mod_name__;
	return this;
}; /* end dynamic */


/* end module: dynamic */
"""

PYJS_INIT = """
$p = $pyjs.loaded_modules["pyjslib"];
$p('pyjslib');
"""

def get_runtime():
    import pyjs
    PYJS_ROOT = os.path.dirname(pyjs.__file__)
    
    def read_file(filename):
        path = os.path.join(PYJS_ROOT, filename)
        return open(path).read()
        
    def compile_file(filename):
        path = os.path.join(PYJS_ROOT, filename)
        return pyjs_translate(open(path).read(), path)
    
    return "\n".join([
        PYJS_BOOTSTRAP,
        read_file("builtin/public/_pyjs.js"),
        compile_file("builtin/pyjslib.py"),
        compile_file("lib/sys.py"),
        PYJS_INIT
    ])
    
def get_runtime_webpy():
    import webpy_ext
    path = os.path.abspath(webpy_ext.__file__)
    if path.endswith(".pyc"):
        path = path[:-1]
    return pyjs_translate(open(path).read(), path)
    
def main():
    from optparse import OptionParser
    parser = OptionParser()
    
    parser.add_option("-e", "--engine", default="webpy",
                      help="Templating engine to use")
    parser.add_option("--runtime", default=False, action="store_true",
                    help="Prints the runtime javascript code required to use the generated js")
    parser.add_option("--runtime-webpy", default=False, action="store_true",
                  help="Prints the runtime javascript code required to use the generated js from webpy templates")
                    
    options, args = parser.parse_args()
    
    if options.runtime:
        print get_runtime()
    elif options.runtime_webpy:
        print get_runtime_webpy()
    else:
        filename = args[0]
        print compile_template(options.engine, open(filename).read(), filename)
