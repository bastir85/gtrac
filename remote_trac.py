#!/usr/bin/env python 
import xmlrpclib

from gi.repository import Gtk

class TicketFetcher():

    def __init__(self,server):
        self.server = xmlrpclib.ServerProxy(server)
        #info                       id, info
        self.store  = Gtk.ListStore(int,str)

    def update_tickets(self):
        ticketids = self.server.ticket.query(self.query)
        multicall = xmlrpclib.MultiCall(self.server)
        [multicall.ticket.get(t) for t in ticketids 
            if t  not in self.current_tickets]
        for res in multicall():
            #res = (id,created,last_changed)
            self.current_tickets[res[0]] = (res[1],res[2],res[3])
        #update storage:
        self.store.clear()
        [self.store.append((k,v[2]['summary'])) for k,v in self.current_tickets.items()]

    def set_query(self,query):
        self.clean()
        self.query = query
        self.update_tickets()

    def clean(self):
        self.current_tickets = {}


