#!/usr/bin/env python
import sys
import os
import logging

from ConfigParser import SafeConfigParser

from gi.repository import Gtk, GdkPixbuf

from xdg.BaseDirectory import save_config_path, xdg_data_dirs

from yapsy.ConfigurablePluginManager import ConfigurablePluginManager
from yapsy.VersionedPluginManager import VersionedPluginManager
from yapsy.PluginManager import PluginManagerSingleton

from widgets import PluginList

class ExampleApp(object):
    """
    Example Application
    
    Main application instance with a single window which demonstrates an example
    of how Yapsy can be used as a framework for plugins in a GTK+ application.
    
    This code is discussed on my blog at: 
    http://www.micahcarrick.com/python-gtk-plugins-with-yapsy.html
    """
    APP_NAME = "yapsy-gtk-example"
    def __init__(self):
        self._create_window()
        
        # Setup a ConfigParser which will be used by the Yapsy plugin manager to
        # remember which plugins are activated. The  function
        # xdg.BaseDirectory.save_config_path() function is used to get the path 
        # for the configuration file. You may want to instead iterate over the
        # xdg.BaseDirectory.xdg_config_dirs if your application installs default
        # configuration files into system directories. See
        # http://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html
        # for more information on the XDG specifications.
        
        self.config = SafeConfigParser()
        config_path = save_config_path(self.APP_NAME)
        self.config_file = os.path.join(config_path, self.APP_NAME + ".conf")
        logging.debug("Reading configuration file: %s" % self.config_file)
        self.config.read(self.config_file)
        
        # Build a list of directories which may contain plugins. This will 
        # include the 'plugins' folder where this file resides as well as every
        # directory in xdg.BaseDirectory.xdg_data_dirs. This way users can
        # install plugins in something like ~/.local/yapsy-gtk-example/plugins
        # but your installer could also install those plugins to something like
        # /usr/share/yapsy-gtk-example/plugins. You'll see Yapsy checking each
        # of these directories if logging is set to logging.DEBUG
        
        this_dir = os.path.abspath(os.path.dirname(__file__))
        plugin_dir = os.path.join(this_dir,'plugins')
        places = [plugin_dir,]
        [places.append(os.path.join(path, self.APP_NAME, "plugins")) for path 
            in xdg_data_dirs]
        
        # The singleton versino of the Yapsy plugin manager is used rather than
        # passing around a PluginManager instance. Prior to getting the 
        # singleton instance, some "plugin manager decorators" are installed to:
        # 1. Automatically save active and non-active plugins to the config file
        # 2. Ensure only the newest versions of plugins are used.
        # This call to setBehaviour() must occur before getting the singleton 
        # instance.
        
        PluginManagerSingleton.setBehaviour([
            ConfigurablePluginManager,
            VersionedPluginManager,
        ])
        
        # Get singleton instance
        manager = PluginManagerSingleton.get()
        
        # I like to give the manager a reference to the application class so
        # that plugins can connect to signals and access windows through
        # the manager singleton. 
        manager.app = self
        
        # Give manager the config file and a callback function to call when it
        # changes the config (eg. when a plugin is activated or deactivated).
        manager.setConfigParser(self.config, self.write_config)
        
        # Setup a file extension for plugin information files. In this it's 
        # just ".plugin" but you may want to do something specific to your
        # application like ".myapp-plugin"
        manager.setPluginInfoExtension("plugin")
        
        # Pass the manager the list of plugin directories
        manager.setPluginPlaces(places)

        # CollectPlugins is a shortcut for locatePlugins() and loadPlugins().
        manager.collectPlugins()
        
        # Now that the plugins have been collected, the plugin widget can
        # be refreshed to display all installed plugins.
        self._plugin_list.refresh()
        
    def _create_window(self):
        """
        Create the main application window and store a reference to it in a
        public property so that plugins can access it.
        """
        self.window = Gtk.Window()
        self.window.set_title("Yapsy Example")
        self.window.set_default_size(400, 400)
        self.window.connect("destroy", lambda w: Gtk.main_quit())
        # PluginList() is a composite widget that shows all installed plugins
        # in a Gtk.TreeView. See widgets.py
        self._plugin_list = PluginList(self.window)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(self._plugin_list, True, True, 0)
        box.show_all()
        self.window.add(box)

    def run(self):
        """
        Run the application by entering the GTK main loop.
        """
        self.window.show()
        Gtk.main()
        
    def write_config(self):
        """
        Write the chances in the ConfigParser to a file.
        """
        logging.debug("Writing configuration file: %s" % self.config_file)
        f = open(self.config_file, "w")
        self.config.write(f)
        f.close()
        
if __name__ == "__main__":
    # Set the loglevel to DEBUG so that we see Yapsy debug messages
    logging.basicConfig(level=logging.DEBUG)
    app = ExampleApp()
    app.run()
    
