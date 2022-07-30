"""Script to reformat the packages listed in the conda output to format suitable for install."""
if __name__ == "__main__":
    with open("/Users/jlewi/tmp/base-cpu:m94") as f:
        
        for l in f.readlines():            
            if l.startswith("Container release"):
                continue
            if l.startswith("#"):
                continue

            pieces = l.split()
            print(f"{pieces[0]}={pieces[1]}")

