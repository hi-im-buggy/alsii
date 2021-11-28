import argparse

def main(args):
    # Store hyp and ref values here
    hyp_list = []
    ref_list = []
    # Open hyp and ref
    with open(args.hyp) as hyp, open(args.ref) as ref:
        # Read line by line in parallel
        for hyp_line, ref_line in zip(hyp, ref):
            # Strip whitespace
            hyp_line = hyp_line.strip()
            ref_line = ref_line.strip()
            # Ignore if both lines are empty
            if not hyp_line and not ref_line: continue
            # Make sure both sides are not empty
            assert hyp_line, ref_line
            # Split each line
            hyp_line = hyp_line.split("\t")
            ref_line = ref_line.split("\t")
            # Extract the predicted values
            hyp_list.append(hyp_line[1])
            ref_list.append(ref_line[1])
            # Detailed printing where the languages do not match
            if args.verbose:
                # Format the output
                format = [repr(hyp_line[0]), hyp_line[1], ref_line[1]]
                # Highlight mismatches
                if hyp_line[1] != ref_line[1]: print("\t".join(format+["ERROR"]))
                else: print("\t".join(format))

    # Make sure hyp and ref are the same length
    assert len(hyp_list) == len(ref_list)
    # Compare hyp and ref and calculate results
    calculateResults(hyp_list, ref_list)

# Input 1: A list of hypothesis values
# Input 2: A list of reference values
# Output 1: An ordered list of unique headings in the confusion matrix
# Output 2: The confusion matrix
# Cf. https://stackoverflow.com/questions/2148543/how-to-write-a-confusion-matrix-in-python
def calculateResults(hyp, ref):
    unique = sorted(set(hyp+ref))
    matrix = [[0 for _ in unique] for _ in unique]
    imap   = {key: i for i, key in enumerate(unique)}
    # Generate Confusion Matrix (predicted, actual)
    for p, a in zip(hyp, ref):
        matrix[imap[p]][imap[a]] += 1
    # Print the confusion matrix
    print("\nCONFUSION MATRIX\n"+"\t".join([""]+unique))
    for i in range(0, len(matrix)):
        print("\t".join([unique[i]]+[str(j) for j in matrix[i]]))

    # Initialise a stats dict
    stats = {}
    # Print header for the class-based micro-F1 score
    print("\n"+"\t".join(["CLASS", "P", "R", "F1"]))
    # Loop through classes and compute statistics
    for i in unique:
        # Add a class dict to the stats dict
        stats[i] = {"tp": 0, "fp": 0, "fn": 0, "p": 0, "r": 0, "f1": 0}
        # Process rows and columns
        loc = matrix[imap[i]][imap[i]]
        row = sum(matrix[imap[i]][:])
        col = sum([row[imap[i]] for row in matrix])
        # Get TP, FP, FN
        tp  = loc
        fp  = row - loc
        fn  = col - loc
        # Get P, R, F1
        p = float(tp) / (tp + fp) if fp else 1.0
        r = float(tp) / (tp + fn) if fn else 1.0
        f1 = float(2 * p * r) / (p + r) if p+r else 0.0
        # Save these in the stats dict
        stats[i]["tp"] = tp
        stats[i]["fp"] = fp
        stats[i]["fn"] = fn
        stats[i]["p"] = round(p * 100, 3)
        stats[i]["r"] = round(r * 100, 3)
        stats[i]["f1"] = round(f1 * 100, 3)
        # Print P, R, F1 for the class
        print("\t".join([i, str(stats[i]["p"]), str(stats[i]["r"]), str(stats[i]["f1"])]))

    # Calculate overall TP, FP, FN
    tp, fp, fn = 0, 0, 0
    # Sum TP, FP, FN of all classes
    for cls_stats in stats.values():
        tp += cls_stats["tp"]
        fp += cls_stats["fp"]
        fn += cls_stats["fn"]
    # Calculate overall P, R, F1
    p = float(tp) / (tp + fp) if fp else 1.0
    r = float(tp) / (tp + fn) if fn else 1.0
    f1 = float(2 * p * r) / (p + r) if p+r else 0.0
    print("-"*30)


if __name__ == "__main__":
    # Define and parse program input
    parser = argparse.ArgumentParser(description="Evaluate Automatic Hindi Annotation")
    parser.add_argument("-hyp", help="Path to a CoNLL hypothesis file.", required=True)
    parser.add_argument("-ref", help="Path to a CoNLL reference file.", required=True)
    parser.add_argument("-v", "--verbose", help="Print the detailed mismatches.", action="store_true")
    args = parser.parse_args()
    # Run the main program.
    main(args)