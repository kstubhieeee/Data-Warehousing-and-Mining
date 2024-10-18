import numpy as np

class Element:
    def __init__(self, n, m):
        self.p = np.zeros((n, m))

class Classifier:
    def __init__(self):
        self.no_attr = 0
        self.no_rows = 0
        self.file_array = []
        self.values = []
        self.class_p = []
        self.a = []
        self.count = 0

    def read_file(self, fname):
        try:
            with open(fname, 'r') as f:
                lines = f.readlines()
        except Exception as e:
            print("ERROR WHILE READING FILE")
            exit(1)
        
        first_line = lines[0].strip().split()
        self.no_attr = len(first_line) - 1
        self.file_array = [line.strip().split() for line in lines]
        self.no_rows = len(self.file_array) - 1

        self.get_all_values()
        self.create_table()
        self.new_entry()

    def in_values(self, col_no, temp):
        for i in range(self.count):
            if self.values[i][col_no] == temp:
                return True
        return False

    def get_all_values(self):
        self.values = [[None for _ in range(self.no_attr + 1)] for _ in range(100)]
        for i in range(self.no_attr + 1):
            for j in range(1, self.no_rows + 1):
                temp = self.file_array[j][i]
                if not self.in_values(i, temp):
                    self.values[self.count][i] = temp
                    self.count += 1
            self.count = 0

    def get_len(self, col_no):
        i = 0
        while self.values[i][col_no] is not None:
            i += 1
        return i

    def create_table(self):
        tp = self.get_len(self.no_attr)
        self.class_p = np.zeros(tp)

        for i in range(tp):
            for j in range(1, self.no_rows + 1):
                if self.values[i][self.no_attr] == self.file_array[j][self.no_attr]:
                    self.class_p[i] += 1

            self.class_p[i] /= self.no_rows
            print(f"P({self.values[i][self.no_attr]}) = {self.class_p[i]}")

        self.a = [None for _ in range(self.no_attr)]
        for i in range(self.no_attr):
            self.a[i] = Element(self.get_len(i), self.get_len(self.no_attr))
            for j in range(self.get_len(i)):
                for k in range(self.get_len(self.no_attr)):
                    tc = 0
                    for x in range(1, self.no_rows + 1):
                        if (self.values[j][i] == self.file_array[x][i] and 
                            self.values[k][self.no_attr] == self.file_array[x][self.no_attr]):
                            tc += 1
                    self.a[i].p[j][k] = tc / self.get_count(self.values[k][self.no_attr], self.no_attr)

    def get_count(self, value, col_no):
        return sum(1 for i in range(1, self.no_rows + 1) if self.file_array[i][col_no] == value)

    def new_entry(self):
        entry = []
        for i in range(self.no_attr):
            entry.append(input(f"Enter {self.file_array[0][i]}: "))

        X = "X=<" + " ".join(entry) + ">"
        print(f"\nThe Unseen Sample is {X}\n")

        p_entry = np.zeros(self.get_len(self.no_attr))
        large = 0.0
        pos = -1
        for i in range(self.get_len(self.no_attr)):
            product = 1.0
            for j in range(self.no_attr):
                product *= self.a[j].p[self.get_index(j, entry[j])][i]
            p_entry[i] = self.class_p[i] * product
            print(f"P(X|{self.values[i][self.no_attr]}).P({self.values[i][self.no_attr]}) = {p_entry[i]}")
            if p_entry[i] > large:
                large = p_entry[i]
                pos = i

        print(f"\nThe Decision is {self.values[pos][self.no_attr]}")

    def get_index(self, col_no, temp):
        for i in range(self.get_len(col_no)):
            if self.values[i][col_no] == temp:
                return i
        print("Invalid Entry")
        return -1

def main():
    c = Classifier()
    fname = input("Enter the Name of the input file with its extension: ")
    c.read_file(fname)

if __name__ == "__main__":
    main()
