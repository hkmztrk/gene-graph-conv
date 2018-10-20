import numpy as np
import pandas as pd
import h5py
import networkx as nx
import academictorrents as at


class GeneInteractionGraph(object):
    def __init__(self, path):
        f = h5py.File(at.get(path))
        self.adj = np.array(f['graph_data']).astype('float32')
        self.node_names = np.array(f['gene_names'])
        self.df = pd.DataFrame(np.array(self.adj))
        self.df.columns = self.node_names
        self.df.index = self.node_names
        self.nx_graph = nx.from_numpy_matrix(self.adj)

    @classmethod
    def get_at_hash(cls, graph_name):
        # This maps between the natural name of a graph and its Academic Torrents hash
        if graph_name == "regnet":
            return "3c8ac6e7ab6fbf962cedb77192177c58b7518b23"
        elif graph_name == "genemania":
            return "ae2691e4f4f068d32f83797b224eb854b27bd3ee"

    def first_degree(self, gene):
        neighbors = set([gene])
        try:
            neighbors = neighbors.union(set(self.nx_graph.neighbors(gene)))
        except Exception as e:
            pass
        neighborhood = np.asarray(nx.to_numpy_matrix(self.nx_graph.subgraph(neighbors)))
        return neighbors, neighborhood

    def bfs_sample_neighbors(self, gene, num_neighbors, include_self=True):
        results = set([])
        if include_self:
            results = set([gene])
        bfs = nx.bfs_edges(self.nx_graph, gene)
        for source, sink in bfs:
            if len(results) == num_neighbors:
                break
            results.add(sink)
        return results
