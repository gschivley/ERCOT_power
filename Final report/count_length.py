import json
import re
import sys

def count_loc(lines):
    """
    Taken from:
    https://app.assembla.com/spaces/tahar/subversion/source/HEAD/tahar.py
    linked to from:
    http://stackoverflow.com/questions/9076672/how-to-count-lines-of-code-in-python-excluding-comments-and-docstrings
    """
    nb_lines  = 0
    docstring = False
    for line in lines:
        line = line.strip()

        if line == "" \
           or line.startswith("#") \
           or docstring and not (line.startswith('"""') or line.startswith("'''"))\
           or (line.startswith("'''") and line.endswith("'''") and len(line) >3)  \
           or (line.startswith('"""') and line.endswith('"""') and len(line) >3) :
            continue

        # this is either a starting or ending docstring
        elif line.startswith('"""') or line.startswith("'''"):
            docstring = not docstring
            continue

        else:
            nb_lines += 1

    return nb_lines


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python get_tutorial_length.py <tutorial .ipynb file>"

    with open(sys.argv[1]) as f:
        data = json.load(f)
    markdown_cells = ["".join(d["source"]) for d in data["cells"] if d["cell_type"] == "markdown"]
    code_cells = [d["source"] for d in data["cells"] if d["cell_type"] == "code"]

    words = len(re.sub(r"\s+", " ", " ".join(markdown_cells)).split(" "))
    loc = sum(count_loc(lines) for lines in code_cells)

    print "Number of words: {}".format(words)
    print "Lines of code: {}".format(loc)