'''
Created on Sep 22, 2010

@author: ivan
'''

import gtk
import logging

from foobnix.fc.fc import FC
from foobnix.util import const
from foobnix.regui.model.signal import FControl
from foobnix.regui.about.about import AboutWindow
from foobnix.util.widget_utils import MenuStyleDecorator
from foobnix.helpers.my_widgets import open_link_in_browser


class MenuBarWidget(FControl):
    def __init__(self, controls, parent=None):
        FControl.__init__(self, controls)
        """TOP menu constructor"""
        
        decorator = MenuStyleDecorator()
        if not parent:
            parent = TopMenuBar() 
        
        top = parent
        
        """File"""
        file = top.add_submenu(_("_File"))
        file.add_image_item(_("Add File(s)"), gtk.STOCK_OPEN, self.controls.on_add_files)
        file.add_image_item(_("Add Folder(s)"), gtk.STOCK_OPEN, self.controls.on_add_folders)
        file.add_image_item(_("Save Playlist As"), gtk.STOCK_SAVE_AS, 
                            lambda: self.controls.notetabs.on_save_playlist(self.controls.notetabs.get_current_tree().scroll))
        file.separator()
        file.add_image_item(_("Quit"), gtk.STOCK_QUIT, self.controls.quit)

        """View"""
        view = top.add_submenu(_("_View"))
        view.set_no_show_all(True)
        self.view_music_tree = view.add_check_item(_("Left Panel"), FC().is_view_music_tree_panel)
        self.view_music_tree.connect("activate", lambda w: controls.layout.set_visible_musictree_panel(w.get_active()))

        self.view_search_panel = view.add_check_item(_("Search Panel"), FC().is_view_search_panel)            
        self.view_search_panel.connect("activate", lambda w: controls.layout.set_visible_search_panel(w.get_active()))

        self.view_cover_lyrics = view.add_check_item(_("Cover & Lyrics Panel"), FC().is_view_coverlyrics_panel)
        self.view_cover_lyrics.connect("activate", lambda w: controls.layout.set_visible_coverlyrics_panel(w.get_active()))
        
        separator1 = view.separator() #@UnusedVariable
        view.add_image_item(_("Equalizer"), None, self.controls.eq.show)
        view.add_image_item(_("Download Manager"), None, self.controls.dm.show)
        separator2 = view.separator()
        preferences_item = view.add_image_item(_("Preferences"), gtk.STOCK_PREFERENCES, self.controls.show_preferences)
        
        """if new style menu - remove preferences from View"""
        if not isinstance(parent, TopMenuBar):
            separator2.hide()
            preferences_item.hide()
        
        """Playback"""
        playback = top.add_submenu(_("_Playback"))

        def set_random(flag=True):            
            FC().is_order_random = flag
            logging.debug("set random" + str(flag))
            controls.os.on_load()

        """Playback - Order"""
        order = playback.add_text_item(_("Order"))
        self.playback_order_linear = order.add_radio_item(_("Linear"), None, not FC().is_order_random)
        self.playback_order_linear.connect("activate", lambda w: set_random(False))
        
        self.playback_order_random = order.add_radio_item(_("Random"), self.playback_order_linear, FC().is_order_random)
        self.playback_order_random.connect("activate", lambda w: set_random(True))
        
        """Playback - Repeat"""
        repeat = playback.add_text_item(_("Repeat"))
        self.lopping_all = repeat.add_radio_item(_("All"), None, FC().repeat_state == const.REPEAT_ALL)
        self.lopping_single = repeat.add_radio_item(_("Single"), self.lopping_all, FC().repeat_state == const.REPEAT_SINGLE)
        self.lopping_disable = repeat.add_radio_item(_("Disable"), self.lopping_all, FC().repeat_state == const.REPEAT_NO)
        
        def repeat_all():
            FC().repeat_state = const.REPEAT_ALL            
            logging.debug("set repeat_all")
            controls.os.on_load()
            
        
        def repeat_sigle():
            FC().repeat_state = const.REPEAT_SINGLE
            logging.debug("set repeat_sigle")
            controls.os.on_load()
        
        def repeat_no():
            FC().repeat_state = const.REPEAT_NO
            logging.debug("set repeat_no")
            controls.os.on_load()
            
        self.lopping_all.connect("activate", lambda * a:repeat_all())
        self.lopping_single.connect("activate", lambda * a:repeat_sigle())
        self.lopping_disable.connect("activate", lambda * a:repeat_no())

        """Playlist View"""
        #playlist = playback.add_text_item("Playlist")
        #self.playlist_plain = playlist.add_radio_item("Plain (normal style)", None, FC().playlist_type == const.PLAYLIST_PLAIN)
        #self.playlist_tree = playlist.add_radio_item("Tree (apollo style)", self.playlist_plain , FC().playlist_type == const.PLAYLIST_TREE)

        #self.playlist_plain.connect("activate", lambda w: w.get_active() and controls.set_playlist_plain())
        #self.playlist_tree.connect("activate", lambda w: w.get_active() and controls.set_playlist_tree())

        """Help"""
        help = top.add_submenu(_("_Help"))
        help.add_image_item(_("About"), gtk.STOCK_ABOUT, self.show_about)
        help.separator()
        help.add_text_item(_("Project page"), lambda * a:open_link_in_browser(_("http://www.foobnix.com/news/eng")), None, False)
        help.add_image_item(_("Issue report"), gtk.STOCK_DIALOG_WARNING, lambda * a:open_link_in_browser("http://code.google.com/p/foobnix/issues/list"))
        help.separator()
        help.add_image_item(_("Donate Participate"), gtk.STOCK_DIALOG_QUESTION, lambda * a:open_link_in_browser(_("http://www.foobnix.com/donate/eng")))
        
        #help.add_image_item("Help", gtk.STOCK_HELP)

        #top.decorate()
        
        decorator.apply(top)
        decorator.apply(file)
        decorator.apply(view)
        decorator.apply(playback)
        decorator.apply(repeat)
        decorator.apply(order)
        decorator.apply(help)
        
        self.widget = top

        self.on_load()
    
    def show_about(self):
        about = AboutWindow()
        about.show()
    
    def on_load(self):
        self.view_music_tree.set_active(FC().is_view_music_tree_panel)
        self.view_search_panel.set_active(FC().is_view_search_panel)
        self.view_cover_lyrics.set_active(FC().is_view_coverlyrics_panel)
                
    def on_save(self):
        FC().is_view_music_tree_panel = self.view_music_tree.get_active()
        FC().is_view_search_panel = self.view_search_panel.get_active()
        FC().is_view_coverlyrics_panel = self.view_cover_lyrics.get_active()
             

class MyMenu(gtk.Menu):
    """My custom menu class for helping buildings"""
    def __init__(self):
        gtk.Menu.__init__(self)

    def add_image_item(self, title, gtk_stock, func=None, param=None):
        item = gtk.ImageMenuItem(title)
        
        
        
        item.show()
        if gtk_stock:
            img = gtk.image_new_from_stock(gtk_stock, gtk.ICON_SIZE_MENU)
            item.set_image(img)

        logging.debug("Menu-Image-Activate" + title + str(gtk_stock) + str(func) + str(param))
        if func and param:
            item.connect("activate", lambda * a: func(param))
        elif func:
            item.connect("activate", lambda * a: func())
        self.append(item)
        return item

    def separator(self):
        separator = gtk.SeparatorMenuItem()
        separator.show()
        self.append(separator)
        return separator

    def add_check_item(self, title, active=False, func=None, param=None):
        check = gtk.CheckMenuItem(title)

        if param and func:
            check.connect("activate", lambda * a: func(param))
        elif func:
            check.connect("activate", lambda * a: func())

        check.show()
        check.set_active(active)
        self.append(check)
        return check

    def add_radio_item(self, title, group, active):
        check = gtk.RadioMenuItem(group, title)
        check.show()
        check.set_active(active)
        self.append(check)
        return check

    def add_text_item(self, title, func=None, param=None, sub_menu=True):
        sub = gtk.MenuItem(title)
        sub.show()
        self.append(sub)
        
        if param and func:
            sub.connect("activate", lambda * a: func(param))
        elif func:
            sub.connect("activate", lambda * a: func())

        if sub_menu:
            menu = MyMenu()
            menu.show()
            sub.set_submenu(menu)
            return menu
        

"""My top menu bar helper"""
class TopMenuBar(gtk.MenuBar):
    def __init__(self):
        rc_st = '''
            style "menubar-style" {
                GtkMenuBar::shadow_type = none
                GtkMenuBar::internal-padding = 0
                }
            class "GtkMenuBar" style "menubar-style"
        '''
        gtk.rc_parse_string(rc_st)
        gtk.MenuBar.__init__(self)

    def add_submenu(self, title):
        menu = MyMenu()
        menu.show()

        file_item = gtk.MenuItem(title)
        file_item.show()

        file_item.set_submenu(menu)
        self.append(file_item)
        return menu


