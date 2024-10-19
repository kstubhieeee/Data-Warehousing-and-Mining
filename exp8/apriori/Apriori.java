package exp8.apriori;

import java.io.*;
import java.util.*;

public class Apriori {

    public static void main(String[] args) {
        AprioriCalculation ap = new AprioriCalculation();
        ap.aprioriProcess();
    }
}

class AprioriCalculation {
    Vector<String> candidates = new Vector<>();
    String configFile = "config.txt";
    String transaFile = "transa.txt";
    String outputFile = "apriori-output.txt";
    int numItems;
    int numTransactions;
    double minSup;
    String[] oneVal;
    String itemSep = " ";

    public void aprioriProcess() {
        Date d;
        long start, end;
        int itemsetNumber = 0;

        getConfig(); // Load configuration
        System.out.println("Apriori algorithm has started.\n");
        d = new Date();
        start = d.getTime(); // Start timer

        // Iteratively generate frequent itemsets
        do {
            itemsetNumber++;
            generateCandidates(itemsetNumber); // Generate candidate itemsets
            calculateFrequentItemsets(itemsetNumber); // Filter frequent itemsets

            if (candidates.size() != 0) {
                System.out.println("Frequent " + itemsetNumber + "-itemsets");
                System.out.println(candidates);
            }
        } while (candidates.size() > 1);

        d = new Date();
        end = d.getTime(); // End timer
        System.out.println("Execution time is: " + ((double) (end - start) / 1000) + " seconds.");
    }

    // Get user input from the console
    public static String getInput() {
        String input = "";
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        try {
            input = reader.readLine();
        } catch (IOException e) {
            System.out.println(e);
        }
        return input;
    }

    // Load configuration from the config file
    private void getConfig() {
        try (BufferedReader data_in = new BufferedReader(new FileReader(configFile))) {
            numItems = Integer.parseInt(data_in.readLine());
            numTransactions = Integer.parseInt(data_in.readLine());
            minSup = Double.parseDouble(data_in.readLine()) / 100.0;
            
            System.out.println("Input configuration: " + numItems + " items, " + numTransactions + " transactions, minsup = " + (minSup * 100) + "%");

            // Initialize oneVal with default '1's or get custom input
            oneVal = new String[numItems];
            System.out.print("Enter 'y' to change the value each row recognizes as a '1': ");
            if ("y".equalsIgnoreCase(getInput())) {
                for (int i = 0; i < oneVal.length; i++) {
                    System.out.print("Enter value for column #" + (i + 1) + ": ");
                    oneVal[i] = getInput();
                }
            } else {
                Arrays.fill(oneVal, "1"); // Default to "1" for all columns
            }
        } catch (IOException e) {
            System.out.println("Error reading configuration: " + e.getMessage());
        }
    }

    // Generate candidate itemsets for iteration n
    private void generateCandidates(int n) {
        Vector<String> tempCandidates = new Vector<>();
        if (n == 1) {
            // Generate individual items as candidates
            for (int i = 1; i <= numItems; i++) {
                tempCandidates.add(Integer.toString(i));
            }
        } else {
            // Generate combinations of itemsets for higher-order sets
            for (int i = 0; i < candidates.size(); i++) {
                String[] tokens1 = candidates.get(i).split(" ");
                for (int j = i + 1; j < candidates.size(); j++) {
                    String[] tokens2 = candidates.get(j).split(" ");
                    if (Arrays.equals(Arrays.copyOfRange(tokens1, 0, n - 2), Arrays.copyOfRange(tokens2, 0, n - 2))) {
                        tempCandidates.add(String.join(" ", tokens1) + " " + tokens2[tokens2.length - 1]);
                    }
                }
            }
        }
        candidates = tempCandidates;
    }

    // Calculate frequent itemsets based on minimum support
    private void calculateFrequentItemsets(int n) {
        Vector<String> frequentCandidates = new Vector<>();
        int[] count = new int[candidates.size()];
        boolean[] trans = new boolean[numItems];

        try (BufferedReader data_in = new BufferedReader(new FileReader(transaFile))) {
            for (int i = 0; i < numTransactions; i++) {
                String[] transaction = data_in.readLine().split(itemSep);
                for (int j = 0; j < numItems; j++) {
                    trans[j] = transaction[j].equalsIgnoreCase(oneVal[j]);
                }

                for (int c = 0; c < candidates.size(); c++) {
                    String[] items = candidates.get(c).split(" ");
                    boolean match = true;
                    for (String item : items) {
                        if (!trans[Integer.parseInt(item) - 1]) {
                            match = false;
                            break;
                        }
                    }
                    if (match) count[c]++;
                }
            }

            // Check which itemsets are frequent
            try (BufferedWriter file_out = new BufferedWriter(new FileWriter(outputFile, true))) {
                for (int i = 0; i < candidates.size(); i++) {
                    if ((double) count[i] / numTransactions >= minSup) {
                        frequentCandidates.add(candidates.get(i));
                        file_out.write(candidates.get(i) + "," + (double) count[i] / numTransactions + "\n");
                    }
                }
                file_out.write("-\n"); // Separator between itemsets
            }
        } catch (IOException e) {
            System.out.println("Error processing transactions: " + e.getMessage());
        }

        candidates = frequentCandidates; // Update candidates with frequent ones
    }
}
