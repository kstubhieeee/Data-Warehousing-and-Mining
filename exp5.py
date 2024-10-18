import math

# Function to calculate Euclidean distance between two points
def distance_to(start, end):
    return math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)

# Function to round to two decimal places
def round2(a):
    if a != float('inf'):
        return round(a, 2)
    return float('inf')

def print_matrix(names, d):
    active_indices = [i for i in range(len(names)) if names[i] != ""]
    max_name_length = max(len(name) for name in names if name != "")
    
    # Print header
    header = f"{'':<{max_name_length}} |"
    for i in active_indices:
        header += f" {names[i]:^10}"
    print(header)
    print("-" * len(header))
    
    # Print rows
    for i in active_indices:
        row = f"{names[i]:<{max_name_length}} |"
        for j in active_indices:
            val = round2(d[i][j]) if d[i][j] != float('inf') else "∞"
            row += f" {val:^10}"
        print(row)

def main():
    # Get the number of points
    N = int(input("Enter N - the number of points: "))
    M = 2  # Number of dimensions (X and Y)
    data = []
    names = []

    # Collect the points
    for i in range(N):
        names.append(f'p{i+1}')
        d = []
        print(f"Enter the coordinates of point {i+1}:")
        for j in range(M):
            d.append(float(input()))
        data.append(d)

    # Display the entered data in a properly formatted table
    print("\nData entered:")
    print(f"{'Point':<10}{'X-coord':<10}{'Y-coord':<10}")
    print("-" * 30)
    for i in range(N):
        print(f"{names[i]:<10}{data[i][0]:<10.2f}{data[i][1]:<10.2f}")

    # Ask for the choice of linkage method
    print("\nEnter your choice: 1. Single linkage, 2. Complete linkage, 3. Average linkage")
    choice = int(input())

    INFINITY = float('inf')
    d = [[INFINITY for _ in range(N)] for _ in range(N)]
    dmin = [0 for _ in range(N)]

    # Initialize distance matrix
    for i in range(N):
        for j in range(i + 1, N):
            if i != j:
                dist = distance_to(data[i], data[j])
                d[i][j] = dist
                d[j][i] = dist
            if d[i][j] < d[i][dmin[i]]:
                dmin[i] = j

    # Display the initial distance matrix
    print("\nInitial Distance Matrix:")
    print_matrix(names, d)

    # Agglomerative clustering process
    for s in range(N - 1):
        # Find the minimum distance pair
        i1 = min(range(N), key=lambda i: d[i][dmin[i]] if i != dmin[i] else INFINITY)
        i2 = dmin[i1]

        print(f"\nPoints {names[i1]} and {names[i2]} are clustered.")
        names[i1] = f"({names[i1]},{names[i2]})"  # Update the cluster name
        names[i2] = ""  # Mark merged cluster

        # Update distances based on the linkage choice
        for j in range(N):
            if j != i1 and j != i2:
                if choice == 1:  # Single linkage
                    d[i1][j] = d[j][i1] = min(d[i1][j], d[i2][j])
                elif choice == 2:  # Complete linkage
                    d[i1][j] = d[j][i1] = max(d[i1][j], d[i2][j])
                elif choice == 3:  # Average linkage
                    d[i1][j] = d[j][i1] = (d[i1][j] + d[i2][j]) / 2

        d[i1][i1] = INFINITY  # Set the diagonal to infinity

        # Set the distances of merged cluster to infinity
        for i in range(N):
            d[i][i2] = d[i2][i] = INFINITY

        # Recalculate minimum distances
        for i in range(N):
            if d[i][dmin[i]] == INFINITY:
                dmin[i] = min(range(N), key=lambda j: d[i][j] if i != j else INFINITY)

        # Print updated distance matrix
        print(f"\nDistance matrix after iteration {s + 1}:")
        print_matrix(names, d)

if __name__ == "__main__":
    main()