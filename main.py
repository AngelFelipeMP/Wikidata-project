# Data manipulation
import pandas as pd
import random

# Wikipedia API
import wikipedia as wp
from wikipedia.exceptions import DisambiguationError, PageError

# Plotting
import networkx as nx
import matplotlib.pyplot as plt


print(wp.summary("data science")[:100])