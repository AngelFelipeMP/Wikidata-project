import os

CODE_PATH = os.getcwd()
REPO_PATH = '/'.join(CODE_PATH.split('/')[0:-1])
LOGS_PATH = REPO_PATH + '/' + 'logs'
GRAPH_FILE = 'links.csv'
PLOT_FILE = 'my_graph.png'

# START_WP = ["Public policy",
#             "Cultural policy",
#             "Economic policy",
#             "Education policy",
#             "Energy policy",
#             "Environmental policy",
#             "Foreign policy",
#             "Health policy",
#             "Immigration policy",
#             "Social policy"]

# N_BRANCH = 10
##DEBUG
START_WP = ["Public policy",
            "Cultural policy",
            "Economic policy"]

N_BRANCH = 2