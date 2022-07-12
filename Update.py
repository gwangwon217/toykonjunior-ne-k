import os

def func1():
    os.system("git clean -n -f -d")
    os.system('git fetch --all')
    os.system("git reset --hard origin/master") 

if __name__ == '__main__':
    # Script2.py executed as script
    # do something
    func1()

