def plugin_start():
   """
   Load this plugin into EDMC
   """
   print "I am loaded!"
   return "Test"

def plugin_stop():
    """
    EDMC is closing
    """
    print "Farewell cruel world!"