Example Using Yapsy Python Plugins with GTK+
============================================

This is an example Python GTK+ application I have been using for experimenting
with [Yapsy](http://yapsy.sourceforge.net/), a simple python plugin system. The
code has a ton of comments and you can read more details on my blog post:
[Python Plugins with Yapsy](http://www.micahcarrick.com/python-gtk-plugins-with-yapsy.html).


Dependencies
------------

* Python 2
* GTK+ 3
* [Yapsy](http://yapsy.sourceforge.net/) - Make sure you grab the Python2 version
and not the Python3 version. Eg. `pip install Yapsy==1.9`
* [PyXDG](http://freedesktop.org/wiki/Software/pyxdg) - Most Linux 
distributions will likely have `pyxdg` or `python-xdg` in their software 
repositories.


Running the Example
-------------------

Launch the application with:

    python yapsy-gtk-example.py
    
Which should show a window like the one below.

![Screenshot of yapsy-gtk-example Window](http://static.micahcarrick.com/media/images/yapsy-gtk-example/screenshot.png)

To get started, take a look at `yapsy-gtk-example.py` first and then look into
the plugin files inside of the `plugins` directory.

