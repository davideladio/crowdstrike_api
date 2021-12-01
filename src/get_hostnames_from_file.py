# many times you'll end up having a file (should be in your files folder)
# with all the hostnames you want to do something with
# first step will be to open that file up and load a list with all those
# hostnames. This can be done several ways. This is how i did it.

hostnames = []

def get_hostnames():
    hn=[]
    with open('../files/hosts.txt') as file_hostnames:
        for line in file_hostnames:
            hn.append(line.rstrip('\n'))
    return hn

hostnames = get_hostnames()