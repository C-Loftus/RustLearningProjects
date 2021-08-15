from pathlib import Path
import os

# quick and dirty script to convert my massive amounts of bash
# aliases to fish


# just copy aliases and only aliases that are simple and 
# share syntax. $() and if [] command syntax is different in fish
def shouldAppendLine(l, configToAppendTo):
    stripped = l.lstrip()
    # not just whitespace
    if len(stripped) > 1:
        #not a comment
        if stripped[0] != '#':
            # contains the word alias and doesn't use nonportable syntax
            if "alias " in l and "$()" not in l and "if" not in l:
                # not repeated
                for line in configToAppendTo:
                    if line == l or line == stripped:
                        return False
                return True
    return False  

def main():
    with open(os.path.join(Path.home() , ".bashrc"), 'r') as bashrc:
        with open(os.path.join(Path.home() , ".config/fish/config.fish"), 'a+') as fish:
            for line in bashrc:
                if shouldAppendLine(line, fish):
                    print("found alias:\n", line)
                    fish.write(line)


if __name__ == "__main__":
    main()
