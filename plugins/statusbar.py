from gi.repository import Gtk

from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton

class HelloStatusbar(IPlugin):
    """
    Hello World Statusbar Plugin
    
    Adds a plugin to the application's window with the text "Hello World". 
    Expects that the PluginManagerSingleton has been assigned a property
    named `app` that contains the `ExampleApp` instance.
    
    Note: In a real world application, you would likely create a base plugin
    class derived from `IPlugin` rather than extending `IPlugin` directly.
    """
    def __init__(self):
        # Make sure to call the parent class (`IPlugin`) methods when 
        # overriding them.
        super(HelloStatusbar, self).__init__()
        
        # The `app` property was added to the manager singleton instance when
        # the manager was setup. See ExampleApp.__init__() in the 
        # yapsy-gtk-example.py file. 
        manager = PluginManagerSingleton.get()
        self.app = manager.app
    
    def activate(self):
        # Make sure to call `activate()` on the parent class to ensure that the
        # `is_activated` property gets set.
        super(HelloStatusbar, self).activate()
        
        # When the plugin is activated (either at startup or with the checkbox
        # in the list) add a statusbar widget to the main window.
        statusbar = Gtk.Statusbar()
        statusbar.push(statusbar.get_context_id("hello"), "Hello World!")
        statusbar.show()
        self.app.window.get_child().pack_start(statusbar, False, True, 0)
        self.statusbar = statusbar
        
    def deactivate(self):
        # Make sure to call `deactivate()` on the parent class to ensure that 
        # the `is_activated` property gets set.
        super(HelloStatusbar, self).deactivate()
        
        # Destroy the statusbar widget when the plugin is deactivated. We don't
        # want stray widgets lingering about.
        self.statusbar.destroy()

