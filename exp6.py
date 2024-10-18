import numpy as np

class KMeans:
    def __init__(self, n_clusters):
        self.n_clusters = n_clusters
        self.centroids = None
        self.clusters = None

    def fit(self, data):
        self.centroids = np.array(data[:self.n_clusters], dtype=float)  # Initial centroids
        self.clusters = [[] for _ in range(self.n_clusters)]

        while True:
            self.clusters = [[] for _ in range(self.n_clusters)]
            
            for point in data:
                distances = np.abs(self.centroids - point)
                cluster = np.argmin(distances)
                self.clusters[cluster].append(point)
            
            old_centroids = np.copy(self.centroids)

            for i in range(self.n_clusters):
                if len(self.clusters[i]) > 0:
                    self.centroids[i] = np.mean(self.clusters[i])

            self.display_step()

            if np.array_equal(self.centroids, old_centroids):
                break

    def display_step(self):

        print("\nAt this step Value of clusters:")
        for i, cluster in enumerate(self.clusters):
            print(f"K{i + 1}{{ {' '.join(map(str, cluster))} }}")
        
        print("Value of m:")
        for i, centroid in enumerate(self.centroids):
            print(f"m{i + 1}={centroid}", end=' ')
        print()

    def print_final_clusters(self):
        print("\nThe Final Clusters By Kmeans are as follows:")
        for i, cluster in enumerate(self.clusters):
            print(f"K{i + 1}{{ {' '.join(map(str, cluster))} }}")

if __name__ == "__main__":
    n = int(input("Enter the number of elements: "))
    data = [int(input(f"Enter element {i + 1}: ")) for i in range(n)]

    p = int(input("Enter the number of clusters: "))

    kmeans = KMeans(n_clusters=p)
    kmeans.fit(data)
    
    kmeans.print_final_clusters()
