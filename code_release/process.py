import argparse
import re

def main(args):
    # Load word lists
    en_words = loadDict("resources/EN.words.txt")
    hi_words = loadDict("resources/HI.trans.fire2013.txt")
    # Load a manually transcribed word map to handle tricky words
    word_map = loadWordMap("resources/word_map.txt", args.top_n)

    # Store resources in a resource dict
    res_dict = {"en": en_words,
                "hi": hi_words,
                "map": word_map}
    # Open output file
    out = open(args.out, "w")
    # Open src token file
    with open(args.conll_file) as tokens:
        # Keep track of the language of the previous token
        # English is the default since there are more en tokens overall.
        prev_lang = "en"
        for tok in tokens:
            tok = tok.strip()
            # Write empty lines to output file and continue
            if not tok:
                # Reset prev_lang
                prev_lang = "en"
                out.write("\n")
                continue
            # Classify token language: en, hi, univ
            lang = assignLang(tok, prev_lang, res_dict)
            # Write to output
            out.write("\t".join([tok, lang])+"\n")
            # Set prev_lang for the next token; IGnore univ since they are rarest
            if lang != "univ": prev_lang = lang 

# Load a list of unique words or syllables from a file.
def loadDict(path):
    words = []
    with open(path) as word_list:
        for line in word_list:
            words.append(line.strip().split("\t")[0])
    return set(words)

# Load a mapping from word to language from a file.
# Input 2: Only store the top n most frequent mappings in the word list.
def loadWordMap(path, top_n):
    map_dict = {}
    # Load everything if top_n is not specified
    if top_n == None: top_n = float("inf")
    with open(path) as word_map:
        for line in word_map:
            line = line.strip().split("\t")
            if len(map_dict) < top_n: map_dict[line[0]] = line[1]
            else: break
    return map_dict

# Input 1: An alphabetical token string
# Input 2: The language of the previous non-universal token: en, hi
# Input 3: A dict of resources
# Output: A language tag: en, hi, univ
def assignLang(tok, prev_lang, res_dict):
    # Check manual wordlist first. Do case insensitive and title case checks.
    if tok in res_dict["map"]: return res_dict["map"][tok]
    elif tok.lower() in res_dict["map"]: return res_dict["map"][tok.lower()]
    elif tok.title() in res_dict["map"]: return res_dict["map"][tok.title()]
    # Punctuation. Note: 19+425 punct tokens are tagged as en and hi in the ref...
    elif re.match('^[\W_]+$', tok): return "univ"
    # Hashtags, shoutouts, URLs and retweet.
    elif "@" in tok or "#" in tok or "http" in tok or tok == "RT": return "univ"
    # Numbers and dates. Underscore is not included in \W
    elif re.sub("[\W_]", "", tok).isdigit(): return "univ"
    # Emoticons; mainly :P, :D and ;)
    elif tok[0] in {":", ";"}: return "univ"
    # Only in English word list (includes some proper nouns)
    elif (tok in res_dict["en"] or tok.title() in res_dict["en"] or tok.lower() in res_dict["en"]) and \
        tok.lower() not in res_dict["hi"]: return "en"
    # Only in Hindi word list
    elif tok.lower() not in res_dict["en"] and tok.lower() in res_dict["hi"]: return "hi"
    # In both or neither list
    else: return prev_lang

if __name__ == "__main__":
    # Define and parse program input
    parser = argparse.ArgumentParser(description="Process Hindi-English Codeswitching text.")
    parser.add_argument("conll_file", help="Path to a CoNLL format input file, 1 token per line.")
    parser.add_argument("-top_n", help="Control size of manual word list to use.", type=int)
    parser.add_argument("-out", help="Output filename.", required=True)
    args = parser.parse_args()
    # Run the main program.
    main(args)