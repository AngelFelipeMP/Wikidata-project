def remove (text, pattern):
	pass

def wiki_ref_extractor(page)
	'''	
	input : wikipedia page title
	Output: list of list of reference templates and text
	'''
	page = extractor(url)
	between_tag = find.all(page, pattern=<ref...<ref/>)
	ref_list = []

	for text in between_tag:
		wikicode = mwparserfromhell.parse(text)
		templates = wikicode.filter_templates()
		
		if templates: 
			text_no_template = remove(text, pattern=template)

			if len(text_no_template) > len(text)*0.2:
				ref_list.append([text, templates, text_no_template])
			else:
				ref_list.append([text, templates])
				
		else:
			ref_list.append([text])

	return ref_list


!! STOP HERE !!
##TODO: Finish code abouve based on my pseudocode (draft)
    ##COMMENTE: base the extraction output from: curl https://api.wikimedia.org/core/v1/wikipedia/en/page/Need
    ## importate links:
		### https://github.com/earwig/mwparserfromhell
		### https://github.com/dissemin/wikiciteparser
		### https://docs.google.com/document/d/1EjjcAOYmOeFea8ZOJDYybaBq5VPyxfzEWeoNugAth0w/edit
		### https://docs.google.com/document/d/1Nc_GUG550FLuqU2xc2CFLCVBc-JXTT2FFsw4TElb9BY/edit
		### https://docs.google.com/document/d/1fhbni6Ylzmk1NYq6kp6rDOL9Gv0ApN5LO9lwOBFqxYw/edit
    
