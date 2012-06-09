from gi.repository import Gtk

from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton

class ConfirmQuit(IPlugin):
    """
    Confirm Quit Plugin
    
    Connects to the window's "delete-event" signal to confirm the user before
    exiting the applicaiton.
    
    Note: In a real world application, you would likely create a base plugin
    class derived from `IPlugin` rather than extending `IPlugin` directly.
    """
    def __init__(self):
        # Make sure to call the parent class (`IPlugin`) methods when 
        # overriding them.
        super(ConfirmQuit, self).__init__()
        
        # The `app` property was added to the manager singleton instance when
        # the manager was setup. See ExampleApp.__init__() in the 
        # yapsy-gtk-example.py file. 
        manager = PluginManagerSingleton.get()
        self.app = manager.app
    
    def activate(self):
        # Make sure to call `activate()` on the parent class to ensure that the
        # `is_activated` property gets set.
        super(ConfirmQuit, self).activate()
        
        # Connect to the "delete-event" and store the handler_id so that the
        # signal handler can be disconnected when the plugin is deactivated.
        # If your plugin connects to multiple signals on multiple objects then
        # you'll want to store the object and the handler_id of each of those.
        self._handler = self.app.window.connect("delete-event", 
                                                self._on_window_delete_event)
    
    def deactivate(self):
        # Make sure to call `deactivate()` on the parent class to ensure that 
        # the `is_activated` property gets set.
        super(ConfirmQuit, self).deactivate()
        
        # Need to disconnect the signal handler when the plugin is deactivated.
        self.app.window.disconnect(self._handler)
    
    def _on_window_delete_event(self, window, event, data=None):
        """
        Show a message dialog prompting the user to confirm that they want to
        quit. Return True if they answer "No" to stop the event from propogating
        and return False if they answer "Yes" to allow the event to occur.        
        """
        dialog = Gtk.MessageDialog(window, Gtk.DialogFlags.MODAL | 
                                           Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                           Gtk.MessageType.QUESTION, 
                                           Gtk.ButtonsType.YES_NO, 
                                           "Are you sure you want to quit?")
        dialog.set_title("Confirm quit")
        r = dialog.run()
        dialog.destroy()
        
        if r == Gtk.ResponseType.YES:
            return False
        else:
            return True

