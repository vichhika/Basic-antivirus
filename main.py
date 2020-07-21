from os import system
from modules.filescan import Filescan
def full_scan(): #task 4
    #scan all partition
    pass
def quick_scan(): #task 2
    #understanding virus behaviour 
    #- regedit
    #- startup
    #- memory
    #- critical directory
    #- quarantine techique #task 1
    pass
def update(): #task 3
    #scraping
    #updatedb
    #update current_update
    #clean
    pass
def custom_scan():
    path = input("Directory path: ")
    print("Scan is preparing ...")
    return Scan.customScan(path)
def menu(num):
    if num == "0": return False
    elif num == "3": return custom_scan()
    else: return True


if __name__ == "__main__":
    # initialize program and update here
    system("cls")
    print("initialize program ...")
    Bool = True
    Scan = Filescan()
    while Bool:
        print("""
██████╗  █████╗ ███████╗██╗ ██████╗          █████╗ ██╗   ██╗
██╔══██╗██╔══██╗██╔════╝██║██╔════╝         ██╔══██╗██║   ██║
██████╔╝███████║███████╗██║██║      █████╗  ███████║██║   ██║
██╔══██╗██╔══██║╚════██║██║██║      ╚════╝  ██╔══██║╚██╗ ██╔╝
██████╔╝██║  ██║███████║██║╚██████╗         ██║  ██║ ╚████╔╝ 
╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝ ╚═════╝         ╚═╝  ╚═╝  ╚═══╝                                                       

1. Quick Scan
2. Full Scan
3. Specific custom scan
4. Update
5. Quarantine
0. Exit

""")   
        choose = input("Choose :")
        Bool = menu(choose)