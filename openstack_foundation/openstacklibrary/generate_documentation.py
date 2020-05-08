import kw_documentation
from robot.libdoc import libdoc
from OpenStackLibrary import OpenStackLibrary

def add_documentation(cls, documentation):
    """Utility method for separating Robot documentation from keyword implementation."""
    methods = list(filter(lambda x: not x.startswith("_"), dir(cls)))
    for method_name in methods:
        method = getattr(cls, method_name)
        if callable(method):
            name = method.__name__
            if hasattr(documentation, name):
                getattr(cls, name).__doc__ = getattr(documentation, name)

add_documentation(OpenStackLibrary, kw_documentation)
libdoc("OpenStackLibrary.py", "documentation.html")
