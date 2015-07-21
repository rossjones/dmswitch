# this is a namespace package
try:
    declare_namespace(__name__)
except NameError:
    print "Failed to declare_namespace()"
