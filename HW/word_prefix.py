import sys

if __name__ == '__main__':

    needle = sys.argv[2]
    longest = ''
    count = 0
    with open(sys.argv[1]) as file:
        for line in file:
            if line.startswith(needle):
                count += 1
                if len(line) > len(longest):
                    longest = line


    print(count)
    print(longest if longest else None)                                                                                                                                                                                                                                                                           

