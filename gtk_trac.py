from gi.repository import Gtk
import pango

from remote_trac import TicketFetcher 
from glib import timeout_add
class SpinnerAnimation(Gtk.Window):

    def __init__(self):

        #trac init 
        url = "https://USER:PWD@url.com"
        self.tickets = TicketFetcher(url)
        query = "group=status&milestone=2.5.0"
        self.tickets.set_query(query)
        self.updater_id = timeout_add(5000,self.update_tickets)

        #window init
        Gtk.Window.__init__(self, title="Spinner")
        self.set_border_width(3)
        self.connect("delete-event", Gtk.main_quit)

        self.button = Gtk.ToggleButton("Start Spinning")
        self.button.connect("toggled", self.on_button_toggled)
        self.button.set_active(False)

        self.spinner = Gtk.Spinner()

        self.tree = Gtk.TreeView(self.tickets.store)
        self.tree.set_headers_visible(False)
        self.tree.set_hover_selection(True)
        
        #self.time_icon_cell = Gtk.CellRendererPixbuf()
        #self.time_icon_cell.set_property("icon-name", "appointment-new")
        #self.time_icon_column = Gtk.TreeViewColumn("", self.time_icon_cell)
        #self.tree.append_column(self.time_icon_column)
        column = Gtk.TreeViewColumn("Tickets")
        t_id   = Gtk.CellRendererText()
        info = Gtk.CellRendererText()

        column.pack_start(t_id, True)
        column.pack_start(info, True)

        column.add_attribute(t_id, "text", 0)
        column.add_attribute(info, "text", 1)
        
        select = self.tree.get_selection()
        #select.set_mode(Gtk.SelectionMode.MULTIPLE)
        self.tree.connect("button-press-event", self.on_tree_button_press_event)
        #select.connect("changed", self.on_tree_selection_changed)

        self.tree.append_column(column)
        '''
        self.activity_column = Gtk.TreeViewColumn("Activity",
                                                    Gtk.CellRendererText(),
                                                    text=1)
        #self.activity_column.set_expand(True)
        self.tree.append_column(self.activity_column)
  
        self.id_cell = Gtk.CellRendererText()
        self.id_cell.set_property('alignment', pango.ALIGN_LEFT)
        self.id_cell.set_property('scale', pango.SCALE_SMALL)
        self.id_cell.set_property('yalign', 0.0)
  
        self.category_column = Gtk.TreeViewColumn("Ticket-ID",
                                                    self.category_cell,
                                                    text=2)
        self.tree.append_column(self.category_column)
        '''
        self.grid = Gtk.Grid()
        self.grid.add(self.spinner)
        self.grid.attach(self.tree,0,3,1,1)
        self.grid.attach(self.button, 0, 2, 1, 1)

        self.add(self.grid)
        self.show_all()

    def on_button_toggled(self, button):
        self.update_tickets()
        return True
    
    def on_tree_button_press_event(self, tree, event):
        model, iter = tree.get_selection().get_selected()
        value = model.get_value(iter, 0)
        Gtk.show_uri(None,"https://trac.yourfirm.de/ticket/%d"%value, event.time)

    def on_tree_selection_changed(self,selection):
        model, treeiter = selection.get_selected()
        if treeiter != None:
            print "You selected", model[treeiter][0]

    def update_tickets(self):
        self.spinner.start()
        self.tickets.update_tickets()
        self.spinner.stop()


myspinner = SpinnerAnimation()

Gtk.main()

