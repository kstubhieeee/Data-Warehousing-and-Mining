import sys

def main():
    # Input for number of transactions
    no_t = int(input("Enter number of transactions: "))
    
    # Input for number of items in the item set
    no_i = int(input("Enter the no. of items in the Item set: "))
    
    # Input for minimum support
    min_sup = int(input("Enter the minimum support: "))

    print("Enter the item set (should be strictly small case alphabets) and Enter 0 once you finish")

    # Initialize the dataset
    d = [[[] for _ in range(2)] for _ in range(no_t)]
    
    # Reading transactions
    for i in range(no_t):
        print(f"TID no: {i + 1}")
        for k in range(no_i):
            s = input()
            d[i][1].append(s)
            if s == "0":
                break

    # Generate item set
    item_set = [chr(i + 97) for i in range(no_i)]
    print("Item Set:")
    print(" ".join(item_set))
    
    # Calculate support for each item
    sup = [0] * no_i
    print("\nCorresponding supports")
    
    for j in range(len(item_set)):
        s = 0
        for i in range(no_t):
            for k in range(no_i):
                if d[i][1][k] == "0":
                    break
                if d[i][1][k][0] == item_set[j]:
                    s += 1
        sup[j] = s
        print(f" {sup[j]}", end="")
    
    # Filter items with support greater than or equal to min_sup
    item_set_new = [''] * no_i
    count = 0
    for k in range(len(sup)):
        if sup[k] >= min_sup:
            item_set_new[k] = item_set[k]
            count += 1
    
    # Sorting items based on support
    for i in range(len(sup)):
        for j in range(len(sup) - 1):
            if sup[j] < sup[j + 1]:
                sup[j], sup[j + 1] = sup[j + 1], sup[j]
                item_set_new[j], item_set_new[j + 1] = item_set_new[j + 1], item_set_new[j]
    
    # Filter out the final item set
    is_final = []
    sup_final = []
    for i in range(no_i):
        if item_set_new[i].isalpha():
            is_final.append(item_set_new[i])
            sup_final.append(sup[i])
    
    # Display final item sets with supports
    print("\n")
    for i in range(len(is_final)):
        print(f"{is_final[i]}\t{sup_final[i]}")
    
    # Print the tree for each transaction
    for i in range(no_t):
        print(f"Transaction No : {i + 1}")
        print("Root")
        for m in range(count):
            for k in range(no_i):
                if d[i][1][k] == "0":
                    break
                if d[i][1][k][0] == is_final[m] and sup_final[m] > 0:
                    print(f"|\n{is_final[m]}")
                    sup_final[m] -= 1
                    break
        print("\n\n")

if __name__ == "__main__":
    main()
