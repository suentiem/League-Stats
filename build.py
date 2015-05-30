import pyinstaller_helper
 
pyinstaller_helper.build({
    'script': 'main.py',
    'application_name': 'League Stats Viewer',
    'version': '1.0.0.0',
    'icon_win': '',
    'company_name': u'',
    'product_name': u'League Stats Viewer',
    'internal_name': 'league_stats_viewer',
    'original_filename': u'League Stats Viewer',
    'file_description': 'Shows stats for League of Legends games and reports via a websocket to listeners',
    'legal_copyright': '',
    'legal_trademark': ''
})