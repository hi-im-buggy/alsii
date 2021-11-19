import argparse

def main(args):
	# Open output file
	out = open(args.conll_file+".new", "w")
	# Tags to simplify
	excep = {"acro", "ne", "mixed", "undef"}
	count_dict = {"en": 0, "hi": 0, "univ": 0}
	# Open input file
	with open(args.conll_file) as input:
		for line in input:
			line = line.strip().split()
			# Simplify language tags
			if line and line[1] in excep: line[1] = "univ"
			out.write("\t".join(line)+"\n")
			if line: count_dict[line[1]] += 1
	print(count_dict)

if __name__ == "__main__":
	# Define and parse program input
	parser = argparse.ArgumentParser(description="Simplify Language tags.")
	parser.add_argument("conll_file", help="Path to a CoNLL format input file, 1 token per line.")
	args = parser.parse_args()
	# Run the main program.
	main(args)