import wx
import gui
import gevent
from threading import Thread, Event
from time import sleep
 
# Extend the gui with some new functionality
class MyFrame(gui.MainFrame):
    def __init__(self, parent, title):
        gui.MainFrame.__init__(self, parent)
 
    # this is the event we defined in wxformbuilder, and now override from gui.py
    def on_button_click_event(self, event):
        print('on_button_click_event')
 
# Create wxpython app
class GuiApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, "League Stats")
        self.SetTopWindow(self.frame)
        self.frame.Show(True)
        print("Gui Created")

        self.frame.Bind(wx.EVT_CLOSE, self.OnClose)
        self.keepGoing = True

        self.set_status_server(False)
        self.set_status_game(False)
        self.set_status_stats(False)
        self.set_status_clients(0)
        self.set_stats({})
 
        return True

    def OnClose(self, event):
        self.keepGoing = False

    def MainLoop(self):
        # Create an event loop and make it active.  If you are
        # only going to temporarily have a nested event loop then
        # you should get a reference to the old one and set it as
        # the active event loop when you are done with this one...
        evtloop = wx.EventLoop()
        old = wx.EventLoop.GetActive()
        wx.EventLoop.SetActive(evtloop)

        # This outer loop determines when to exit the application,
        # for this example we let the main frame reset this flag
        # when it closes.
        while self.keepGoing:
            # At this point in the outer loop you could do
            # whatever you implemented your own MainLoop for.  It
            # should be quick and non-blocking, otherwise your GUI
            # will freeze.  
            # This inner loop will process any GUI events
            # until there are no more waiting.
            while evtloop.Pending():
                evtloop.Dispatch()

            # Send idle events to idle handlers.  You may want to
            # throttle this back a bit somehow so there is not too
            # much CPU time spent in the idle handlers.  For this
            # example, I'll just snooze a little...
            gevent.sleep(0.1)
            self.ProcessIdle()
        wx.EventLoop.SetActive(old)

    def set_status_server(self, status):
        self.frame.m_status_server.SetValue(status)

    def set_status_game(self, status):
        self.frame.m_status_game.SetValue(status)

    def set_status_stats(self, status):
        self.frame.m_status_stats.SetValue(status)

    def set_status_clients(self, total):
        self.frame.m_status_clients.SetLabel(str(total))

    def set_stats(self, stats):
        self.frame.m_stats_player_cs.SetLabel(str(stats.get('CS', '?')))
        self.frame.m_stats_player_kills.SetLabel(str(stats.get('kills', '?')))
        self.frame.m_stats_player_deaths.SetLabel(str(stats.get('deaths', '?')))
        self.frame.m_stats_player_assists.SetLabel(str(stats.get('assists', '?')))
        self.frame.m_stats_team_kills.SetLabel(str(stats.get('team_kills', '?')))
        self.frame.m_stats_team_deaths.SetLabel(str(stats.get('team_deaths', '?')))

class Gui():
    def __init__(self, death_event, **kwargs):
        self.death_event = death_event
        self.app = GuiApp(redirect=False)
        self.run_thread = Thread(target=Gui.run_gui, args=(self.app, self.death_event))

    def start(self):
        self.run_thread.start()

    @staticmethod
    def run_gui(app, kill_event):
        app.MainLoop()
        kill_event.set()


    # =========================================
    #  Interface setting
    # =========================================

    def set_status_server(self, status):
        self.app.set_status_server(status)

    def set_status_game(self, status):
        self.app.set_status_game(status)

    def set_status_stats(self, status):
        self.app.set_status_stats(status)

    def set_status_clients(self, total):
        self.app.set_status_clients(total)

    def set_stats(self, stats):
        self.app.set_stats(stats)