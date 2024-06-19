import pandas
from scipy.stats import iqr

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

def find_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node, _ in graph[start]:
        if node not in path:
            newpaths = find_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def path_length(graph, path):
    length = 0
    for i in range(len(path) - 1):
        for node, dist in graph[path[i]]:
            if node == path[i+1]:
                length += dist
                break
    return length

graph = {}
for i, row in explorer_df.iterrows():
    start, end, distance = row['noeud_amont'], row['noeud_aval'], row['distance']
    if start in graph:
        graph[start].append((end, distance))
    else:
        graph[start] = [(end, distance)]


all_paths = []
for start in graph:
    for end in graph:
        if start != end:
            for path in find_paths(graph, start, end):
                all_paths.append((path, path_length(graph, path)))

def find_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node, _ in graph[start]:
        if node not in path:
            newpaths = find_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def calculate_statistics(lengths):
    average_length = sum(lengths) / len(lengths)
    median_length = pandas.Series(lengths).median()
    std_dev_length = pandas.Series(lengths).std()
    iqr_length = iqr(lengths)
    return average_length, median_length, std_dev_length, iqr_length


def identify_extreme_paths(all_paths):
    longest_path = max(all_paths, key=lambda x: x[1])
    shortest_path = min(all_paths, key=lambda x: x[1])
    return longest_path, shortest_path

def main():
    longest_path, shortest_path = identify_extreme_paths(all_paths)

    lengths = [length for _, length in all_paths]
    average_length, median_length, std_dev_length, iqr_length = calculate_statistics(lengths)

    print("Chemin le plus long :", longest_path)
    print("Chemin le plus court :", shortest_path)
    print("Longueur moyenne des chemins :", average_length)
    print("Longueur médiane des chemins :", median_length)
    print("Écart type des longueurs des chemins :", std_dev_length)
    print("Intervalle interquartile des longueurs des chemins :", iqr_length)

if __name__ == "__main__":
    main()

