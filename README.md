# Wikipedia, reliable sources and public policy issues: Investigating the role of organisation publishing

![ScreenShot](image/yes_to_evidence_based_policy.png)

## Project Summary

A key part of Wikimedia’s defence system against mis/disinformation is its content and citation policies however Wikipedia’s reliable sources policies are still grounded in traditional notions of the research publishing economy as primarily commercial and scholarly publishers and mainstream news media. This is problematic for public policy and public interest topics which tends to have a more diverse media economy of sources, including organisations based in government, civil society, education and commercial sectors, and genres such as reports, policy briefs, fact sheets and datasets.

Public policy is a complex, dynamic and multicentric environment and this is reflected in the diverse publishing ecosystem producing policy-related research including International NGOs, national government agencies, think tanks and research centres. Publications produced by organizations (grey literature) are often more timely and accessible and provide perspectives from community and Indigenous organizations, however some are also partisan and funded by commercial or vested interests – making evaluation of sources challenging.

This research project seeks to understand the extent that policy research reports and papers from organisations are being cited on Wikipedia, what kinds of sources are being cited and how can editors and readers be supported in evaluating their credibility. It will analyse and extend existing research from English Wikipedia (including Avieson 2022; Ford et al. 2013; Lewoniewski 2022; Luyt 2021; Singh et al. 2021; Wong et al. 2021) and the Missing Link Project undertaken by [Analysis & Policy Observatory](https://apo.org.au/), funded by a WMF Alliance grant in 2022. 

The research will involve mapping organisations and genres across key topics on English Wikipedia including analysis by location, topic area, sector and genre, and provide recommendations for improving guidelines that better reflect the complexity of the research publishing ecosystem. Wikidata will also be used to analyse and collect data, classify policy sources and genres and visualise key policy networks.

The project will provide new insights not only for Wikimedia but also for the wider evidence and policy research community. It will also help to strengthen Wikipedia’s verifiability processes and Wikimedia’s role as a leader in digital and media literacy and education – helping to deliver the WMF 2030 Movement Strategy and supporting Wikimedia's ongoing role in providing essential infrastructure and content for the free knowledge ecosystem.

## Repository Overview
This repository houses the code for the project [Wikipedia, reliable sources and public policy issues: Investigating the role of organisation publishing](https://sites.google.com/view/wp-sources-public-policy). We have written these scripts to create a Knowledge Graph from the public policy domain using Wikipedia pages and then extract the references out of those pages.

# System Usage Guide

Before you begin, ensure that you have Python installed on your system. Additionally, the required libraries must be installed through pip:

```bash
pip install pandas networkx matplotlib wikipedia icecream
```

The code may be runned in following sequence:

`1) knowledge_graph.py`

    input:
        -> Wikipedia pages (Wiki API)
    output:
        -> Graph shaped as a table: 'links_official.csv'
        -> Simplified image of the graph: 'plot_simplified_graph.png'

`2) rank_and_qid.py`
    
    input:
        -> Graph table: 'links_official.csv'
    output:
        -> Ranked table with Qids: 'links_plus_qids_official.csv'

`3) collect_wiki_pages`

    input:
        standar: 'links_plus_qids.csv'
    output:
        -> Wikipedia pages text sorce (.json)
        -> logs:
            -> not_found_wiki_pages.csv (only it the script miss a wiki page)
            -> files_with_redirect-target.csv
            -> files_without_source.csv

`4) extract_refs_v5.py`

    input:
        -> Wikipedia pages text sorce (.json)
    output:
        -> 'wikipedia_references.csv'
        -> 'wikipedia_number_of_references.csv'

## Knowledge Graph 
The `Knowledge_graph.py` script can take several arguments:

- `--wp`: Specify one or more Wikipedia page titles to start creating the graph.
- `--branch`: Set the number of extra branches to scan. Default is no additional branching.
- `--path`: Provide the full path to save output files. Defaults to project's predefined paths.
- `--official`: If set, use the official Wikipedia project parameters for graph creation.
- `--plot`: Generate and display a visualization of the simplified knowledge graph.

To see a help message with available arguments, run:
```bash
python Knowledge_graph.py --help
```

### Running the Script

Here are some examples of how to run the script with various options:

**Creating a Graph from Specific Wikipedia Pages:**
```bash
python Knowledge_graph.py --wp "Python (programming language)" --wp "Artificial Intelligence" --plot
```

**Branching Out from a Page Multiple Times:**
```bash
python Knowledge_graph.py --wp "Machine Learning" --branch 5 --plot
```

**Using Predefined Official Parameters and Saving to a Specific Path:**
```bash
python Knowledge_graph.py --official --path "/path/to/save/files"
```

## Ranking and adding Qid
.....

## Collecting Wiki pages
.....

## Extracting References
.....


## Contact

For questions, collaborations, or contributions, please feel free to open an issue or submit a pull request.

## License

 Apache 2.0











 <!-- ### Understanding the Script

The `Knowledge_graph.py` script relies on functions defined in `utils.py`. Here's a brief overview of the components:

### RelationshipGenerator Class

The core of the logic lies within the `RelationshipGenerator` class, which:

1. Scans content of Wikipedia pages to generate relationships between terms.
2. Stores links (relationships) with weights indicating their strength/importance.

### Functions in utils.py

- `clean_links`: Removes non-existing links and corrects link titles.
- `simplify_graph`: Trims down the graph to keep only the most significant nodes.
- `plot_graph`: Plots the knowledge graph using Matplotlib and NetworkX.
- `simplified_plot`: Generates a simplified version of a larger graph and plots it.

### Configuration

Some parameters for graph creation can be set in a separate `config` module. This may include file paths, constants for graph simplification, and default starting points.

## Plotting the Graph

If the `--plot` argument is used, the script will generate a visualization of the simplified knowledge graph. The plotted graph displays nodes, weighted edges, and labels to provide insights into different connections between the topics.

The resulting plot image will be saved in the same directory as the output files (the graph data), unless otherwise specified.

## Conclusion

This script is a powerful tool for exploring and visualizing relationships between concepts on Wikipedia. By adjusting the input arguments, you can customize the breadth and depth of the knowledge graph created to suit your research needs. -->