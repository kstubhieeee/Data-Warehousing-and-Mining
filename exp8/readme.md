
## Steps to Run the Program

### 1. Copy Your Files into a Folder

Ensure your project folder has the following structure:

```
/exp8
   ├── apriori/
   │     └── Apriori.java
   ├── config.txt
   ├── transa.txt
   └── apriori-output.txt (will be generated after running the program)
```

### 2. Compile the Program

Navigate to the folder containing the files and compile the Java program:

```bash
javac apriori/Apriori.java
```

### 3. Run the Program

Execute the compiled program with the following command:

```bash
java apriori.Apriori
```

### 4. Provide User Input

When prompted by the program, you can enter the following example inputs:

```bash
Enter 'y' to change the value each row recognizes as a '1': y
Enter value for column #1: 1
Enter value for column #2: 2
Enter value for column #3: 3
Enter value for column #4: 1
Enter value for column #5: 1
```

### 5. View the Results

The program will output frequent itemsets in the terminal and save them to the `apriori-output.txt` file, which will be generated in the same folder.

---
