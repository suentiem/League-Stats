# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"League Stats", pos = wx.DefaultPosition, size = wx.Size( 421,137 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel26 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel26.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )
		
		bSizer44 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel25 = wx.Panel( self.m_panel26, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer36 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel25, wx.ID_ANY, u"Server" ), wx.HORIZONTAL )
		
		
		sbSizer1.AddSpacer( ( 10, 0), 1, wx.EXPAND, 5 )
		
		self.m_status_server = wx.RadioButton( self.m_panel25, wx.ID_ANY, u"Server", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_status_server.Enable( False )
		
		sbSizer1.Add( self.m_status_server, 0, wx.BOTTOM, 5 )
		
		
		sbSizer1.AddSpacer( ( 10, 0), 1, wx.EXPAND, 5 )
		
		self.m_status_game = wx.RadioButton( self.m_panel25, wx.ID_ANY, u"Game", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_status_game.Enable( False )
		
		sbSizer1.Add( self.m_status_game, 0, 0, 5 )
		
		
		sbSizer1.AddSpacer( ( 10, 0), 1, wx.EXPAND, 5 )
		
		self.m_status_stats = wx.RadioButton( self.m_panel25, wx.ID_ANY, u"Stats", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_status_stats.Enable( False )
		
		sbSizer1.Add( self.m_status_stats, 0, 0, 5 )
		
		
		sbSizer1.AddSpacer( ( 10, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticText106 = wx.StaticText( self.m_panel25, wx.ID_ANY, u"Clients:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText106.Wrap( -1 )
		sbSizer1.Add( self.m_staticText106, 0, wx.RIGHT, 5 )
		
		self.m_status_clients = wx.StaticText( self.m_panel25, wx.ID_ANY, u"123", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_status_clients.Wrap( -1 )
		self.m_status_clients.SetMinSize( wx.Size( 30,-1 ) )
		self.m_status_clients.SetMaxSize( wx.Size( 30,-1 ) )
		
		sbSizer1.Add( self.m_status_clients, 0, 0, 5 )
		
		
		sbSizer1.AddSpacer( ( 10, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer36.Add( sbSizer1, 1, wx.EXPAND, 5 )
		
		
		bSizer36.AddSpacer( ( 10, 0), 1, wx.EXPAND, 5 )
		
		bSizer34 = wx.BoxSizer( wx.HORIZONTAL )
		
		sbSizer8 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel25, wx.ID_ANY, u"Player" ), wx.HORIZONTAL )
		
		self.m_staticText1061 = wx.StaticText( self.m_panel25, wx.ID_ANY, u"Kills:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1061.Wrap( -1 )
		sbSizer8.Add( self.m_staticText1061, 0, wx.RIGHT|wx.LEFT, 5 )
		
		self.m_stats_player_kills = wx.StaticText( self.m_panel25, wx.ID_ANY, u"123", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_stats_player_kills.Wrap( -1 )
		self.m_stats_player_kills.SetMinSize( wx.Size( 25,-1 ) )
		self.m_stats_player_kills.SetMaxSize( wx.Size( 25,-1 ) )
		
		sbSizer8.Add( self.m_stats_player_kills, 0, 0, 5 )
		
		self.text11 = wx.StaticText( self.m_panel25, wx.ID_ANY, u"Deaths:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.text11.Wrap( -1 )
		sbSizer8.Add( self.text11, 0, wx.RIGHT, 5 )
		
		self.m_stats_player_deaths = wx.StaticText( self.m_panel25, wx.ID_ANY, u"123", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_stats_player_deaths.Wrap( -1 )
		self.m_stats_player_deaths.SetMinSize( wx.Size( 25,-1 ) )
		self.m_stats_player_deaths.SetMaxSize( wx.Size( 25,-1 ) )
		
		sbSizer8.Add( self.m_stats_player_deaths, 0, 0, 5 )
		
		self.text12 = wx.StaticText( self.m_panel25, wx.ID_ANY, u"Assists:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.text12.Wrap( -1 )
		sbSizer8.Add( self.text12, 0, wx.RIGHT, 5 )
		
		self.m_stats_player_assists = wx.StaticText( self.m_panel25, wx.ID_ANY, u"123", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_stats_player_assists.Wrap( -1 )
		self.m_stats_player_assists.SetMinSize( wx.Size( 25,-1 ) )
		self.m_stats_player_assists.SetMaxSize( wx.Size( 25,-1 ) )
		
		sbSizer8.Add( self.m_stats_player_assists, 0, 0, 5 )
		
		self.text13 = wx.StaticText( self.m_panel25, wx.ID_ANY, u"CS:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.text13.Wrap( -1 )
		sbSizer8.Add( self.text13, 0, wx.RIGHT, 5 )
		
		self.m_stats_player_cs = wx.StaticText( self.m_panel25, wx.ID_ANY, u"123", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_stats_player_cs.Wrap( -1 )
		self.m_stats_player_cs.SetMinSize( wx.Size( 25,-1 ) )
		self.m_stats_player_cs.SetMaxSize( wx.Size( 25,-1 ) )
		
		sbSizer8.Add( self.m_stats_player_cs, 0, 0, 5 )
		
		
		bSizer34.Add( sbSizer8, 1, wx.EXPAND, 5 )
		
		
		bSizer34.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		sbSizer81 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel25, wx.ID_ANY, u"Team" ), wx.HORIZONTAL )
		
		self.m_staticText10611 = wx.StaticText( self.m_panel25, wx.ID_ANY, u"Kills:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10611.Wrap( -1 )
		sbSizer81.Add( self.m_staticText10611, 0, wx.RIGHT|wx.LEFT, 5 )
		
		self.m_stats_team_kills = wx.StaticText( self.m_panel25, wx.ID_ANY, u"123", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_stats_team_kills.Wrap( -1 )
		self.m_stats_team_kills.SetMinSize( wx.Size( 25,-1 ) )
		self.m_stats_team_kills.SetMaxSize( wx.Size( 25,-1 ) )
		
		sbSizer81.Add( self.m_stats_team_kills, 0, 0, 5 )
		
		self.text21 = wx.StaticText( self.m_panel25, wx.ID_ANY, u"Deaths:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.text21.Wrap( -1 )
		sbSizer81.Add( self.text21, 0, wx.RIGHT, 5 )
		
		self.m_stats_team_deaths = wx.StaticText( self.m_panel25, wx.ID_ANY, u"123", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_stats_team_deaths.Wrap( -1 )
		self.m_stats_team_deaths.SetMinSize( wx.Size( 25,-1 ) )
		self.m_stats_team_deaths.SetMaxSize( wx.Size( 25,-1 ) )
		
		sbSizer81.Add( self.m_stats_team_deaths, 0, 0, 5 )
		
		
		bSizer34.Add( sbSizer81, 1, wx.EXPAND, 5 )
		
		
		bSizer36.Add( bSizer34, 1, wx.EXPAND, 5 )
		
		
		self.m_panel25.SetSizer( bSizer36 )
		self.m_panel25.Layout()
		bSizer36.Fit( self.m_panel25 )
		bSizer44.Add( self.m_panel25, 1, wx.EXPAND|wx.ALL, 8 )
		
		
		self.m_panel26.SetSizer( bSizer44 )
		self.m_panel26.Layout()
		bSizer44.Fit( self.m_panel26 )
		bSizer1.Add( self.m_panel26, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

