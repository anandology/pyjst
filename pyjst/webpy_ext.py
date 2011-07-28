def escape_(text):
    if value is None: 
        value = ''
    return htmlquote(str(text))

def htmlquote(text):
    r"""
    Encodes `text` for raw use in HTML.

        >>> htmlquote(u"<'&\">")
        u'&lt;&#39;&amp;&quot;&gt;'
    """
    text = text.replace(u"&", u"&amp;") # Must be done first!
    text = text.replace(u"<", u"&lt;")
    text = text.replace(u">", u"&gt;")
    text = text.replace(u"'", u"&#39;")
    text = text.replace(u'"', u"&quot;")
    return text
    
class ForLoop:
    def setup(self, it):
        return it
    
class TemplateResult(object):
    """Dictionary like object for storing template output.

    The result of a template execution is usally a string, but sometimes it
    contains attributes set using $var. This class provides a simple
    dictionary like interface for storing the output of the template and the
    attributes. The output is stored with a special key __body__. Convering
    the the TemplateResult to string or unicode returns the value of __body__.

    When the template is in execution, the output is generated part by part
    and those parts are combined at the end. Parts are added to the
    TemplateResult by calling the `extend` method and the parts are combined
    seemlessly when __body__ is accessed.

        >>> d = TemplateResult(__body__='hello, world', x='foo')
        >>> d
        <TemplateResult: {'__body__': 'hello, world', 'x': 'foo'}>
        >>> print d
        hello, world
        >>> d.x
        'foo'
        >>> d = TemplateResult()
        >>> d.extend([u'hello', u'world'])
        >>> d
        <TemplateResult: {'__body__': u'helloworld'}>
    """
    def __init__(self, *a, **kw):
        self._d = dict(*a, **kw)
        self._d.setdefault("__body__", u'')

        self._parts = []
        self.extend = self._parts.extend

        self._d.setdefault("__body__", None)

    def keys(self):
        return self._d.keys()

    def _prepare_body(self):
        """Prepare value of __body__ by joining parts.
        """
        if self._parts:
            value = u"".join(self._parts)
            self._parts[:] = []
            body = self._d.get('__body__')
            if body:
                self._d['__body__'] = body + value
            else:
                self._d['__body__'] = value

    def __getitem__(self, name):
        if name == "__body__":
            self._prepare_body()
        return self._d[name]

    def __setitem__(self, name, value):
        if name == "__body__":
            self._prepare_body()
        return self._d.__setitem__(name, value)

    def __delitem__(self, name):
        if name == "__body__":
            self._prepare_body()
        return self._d.__delitem__(name)

    def __getattr__(self, key): 
        try:
            return self[key]
        except KeyError, k:
            raise AttributeError, k

    def __unicode__(self):
        self._prepare_body()
        return self["__body__"]

    def __str__(self):
        self._prepare_body()
        return self["__body__"]

    def __repr__(self):
        self._prepare_body()
        return "<TemplateResult: %s>" % self._d

