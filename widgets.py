import os
from gi.repository import Gtk, GObject, GdkPixbuf
from yapsy.PluginManager import PluginManagerSingleton

class PluginList(Gtk.Box):
    __gtype_name__ = "PluginManager"
    """
    A composite widget which contains a tree view of installed plugins allowing
    a user to activate and de-activate the plugins and a toolbar to view the
    plugin information and refresh the list.
    """
    def __init__(self, parent=None):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.parent = parent
        
        # toolbar
        toolbar = Gtk.Toolbar()
        toolbar.set_icon_size(Gtk.IconSize.MENU)
        
        button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_REFRESH)
        button.connect("clicked", self._on_refresh_clicked)
        toolbar.insert(button, -1)
        
        toolbar.insert(Gtk.SeparatorToolItem.new(), -1)
        
        button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_ABOUT)
        button.set_sensitive(True)
        button.connect("clicked", self._on_about_clicked)
        toolbar.insert(button, -1)
        
        self.pack_start(toolbar, False, True, 0)
        
        # plugin list
        self._treeview = PluginTreeView()
        sw = Gtk.ScrolledWindow()
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        sw.add(self._treeview)
        
        self.pack_start(sw, True, True, 0)
        self.show_all()
        
    def _on_about_clicked(self, toolbutton, data=None):
        """ Show an 'About' dialog. """
        selection = self._treeview.get_selection()
        model, iter = selection.get_selected()
        if iter:
            info = model[iter][4]
            dialog = Gtk.AboutDialog()
            dialog.set_transient_for(self.parent)
            dialog.set_modal(True)
            dialog.set_authors((info.author,))
            dialog.set_website(info.website)
            dialog.set_website_label(info.website)
            dialog.set_program_name(info.name)
            dialog.set_version(str(info.version))
            dialog.set_comments(info.description)
            dialog.run()
            dialog.destroy()

    def _on_refresh_clicked(self, toolbutton, data=None):
        self._treeview.refresh()
    
    def refresh(self):
        self._treeview.refresh()
        
class PluginTreeView(Gtk.TreeView):
    __gtype_name__ = "PluginTreeView"
    """
    A Gtk.TreeView widget populated with installed plugins allowing a user to
    activate and deactivate the plugins.     
    """
    plugin_icon = None
        
    def __init__(self):
        
        self._store = Gtk.ListStore(GObject.TYPE_BOOLEAN,   # activated
                                    GdkPixbuf.Pixbuf,       # icon
                                    GObject.TYPE_STRING,    # name
                                    GObject.TYPE_STRING,    # version
                                    object)                 # plugin info               
        Gtk.TreeView.__init__(self, self._store)
        self.set_headers_visible(True)          
        self.get_selection().set_mode(Gtk.SelectionMode.BROWSE)
        
        column = Gtk.TreeViewColumn("Plugin")
        cell = Gtk.CellRendererToggle()
        cell.connect("toggled", self._on_active_toggled)
        column.pack_start(cell, True)
        column.add_attribute(cell, 'active', 0)
        cell = Gtk.CellRendererPixbuf()
        column.pack_start(cell, False)
        column.add_attribute(cell, 'pixbuf', 1)
        cell = Gtk.CellRendererText()
        column.pack_start(cell, True)
        column.add_attribute(cell, 'text', 2)
        self.append_column(column)
        
        column = Gtk.TreeViewColumn("Version")
        cell = Gtk.CellRendererText()
        column.pack_start(cell, True)
        column.add_attribute(cell, 'text', 3)
        self.append_column(column)
        
        this_dir = os.path.abspath(os.path.dirname(__file__))
        icon_file = os.path.join(this_dir, "plugin.png")
        self.plugin_icon = GdkPixbuf.Pixbuf.new_from_file(icon_file)
    
    def _on_active_toggled(self, cell, path, data=None):
        # toggle the check box
        iter = self._store.get_iter(path)
        self._store[iter][0] = not self._store[iter][0]
        
        # activate or deactivate the plugin
        manager = PluginManagerSingleton.get()
        if self._store[iter][0]:
            manager.activatePluginByName(self._store[iter][4].name)
        else:
            manager.deactivatePluginByName(self._store[iter][4].name)
        
    def refresh(self):
        self._store.clear()
        manager = PluginManagerSingleton.get()
        for info in manager.getAllPlugins():
            plugin = info.plugin_object
            self._store.append((plugin.is_activated, self.plugin_icon, info.name, 
                                str(info.version), info))
        if len(self._store):
            self.get_selection().select_iter(self._store.get_iter_first())
