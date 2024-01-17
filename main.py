import pandas

explorer_df = pandas.read_csv("./parcours_explorateurs.csv")

"""
Une liste qui contient les noeuds de départ <= filtrer un dataframe
Une liste qui contient les noeuds d'arrivée <= filtrer un dataframe
Un dictionnaire qui associe des noeuds amonts à des noeuds avals 
"""
array_starting_node = explorer_df[explorer_df["type_aretes"]=="depart"]["noeud_amont"].values
array_arrival_node = explorer_df[explorer_df["type_aretes"]=="arrivee"]["noeud_aval"].values
dict_upstream_downstream = {row["noeud_amont"] : row["noeud_aval"] for _, row in explorer_df.iterrows()}


for starting_node in array_starting_node:
	"""
	chaque itération de cette boucle for permet de construire le chemin d'un explorateur.
	pour chacun des explorateurs :
		+ nous allons une liste contenant l'ensemble des sommets par lesquelles il est passé.
		+ nous commençons par le noeud de départ de l'explorateur courrant
		+ via le dictionnaire nous pouvons réccupérer le noeud aval du noeud courant
		+ la construction se fait via un processus itératif qui s'arrête quand le noueud courant à l'array 
		contenant le dernier sommet
	"""
	current_path = [starting_node]
	while current_path[-1] not in array_arrival_node:
		current_node = current_path[-1]
		next_node = dict_upstream_downstream[current_node]

		current_path.append(next_node)

	print(current_path)










#comment looper sur les clefs et valeurs d'un dictionnaire
# for upstream, downstream in dict_upstream_downstream.items():
# 	print(upstream, downstream)

