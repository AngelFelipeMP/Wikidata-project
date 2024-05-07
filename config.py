import os

CODE_PATH = os.getcwd()
REPO_PATH = '/'.join(CODE_PATH.split('/')[0:-1])
LOGS_PATH = REPO_PATH + '/' + 'logs'
WIKI_PAGES = REPO_PATH + '/''wiki_pages'
LOGS_WIKI_PAGES = WIKI_PAGES + '/' + 'logs'
GRAPH_FILE = 'links.csv'
PLOT_FILE = 'my_graph.png'

START_WP = ["Public policy",
            "Cultural policy",
            "Economic policy",
            "Education policy",
            "Energy policy",
            "Environmental policy",
            "Foreign policy",
            "Health policy",
            "Immigration policy",
            "Social policy"]

N_BRANCH = 10