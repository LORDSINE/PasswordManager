from vault.storage import VaultStorage
from tabulate import tabulate

def main():
    storage = VaultStorage()

    print("CLI Password Manager.\nVersion:0.1.0\nDeveloped on September 2025")
    print("Developed by LORDSINE")
    print("\nCommands:- add, get, list, delete, exit")

    while True:
        cmd = input("vault> ").strip().lower()

        if cmd == "add":
            service = input("     > Service: ")
            username = input("     > Username: ")
            password = input("     > Password: ")
            storage.add_entry(service, username, password)
            print("New Entry Saved!!!")

        elif cmd == "get":
            service = input("     > Service: ")
            entry = storage.get_entry(service)
            if entry:
                headers = ["Service", "Username", "Password"]
                table = [[service, entry[0], entry[1]]]
                print(tabulate(table, headers, tablefmt="fancy_grid"))
            else:
                print("No data found!")

        elif cmd == "list":
            services = storage.list()
            if services:
                headers = ["Stored Services"]
                table = [[svc] for svc in services]
                print(tabulate(table, headers, tablefmt="fancy_grid"))
            else:
                print("No services saved yet.")

        elif cmd == "delete":
            service = input("     > Service: ")
            storage.delete(service)
            print("Deleted (if existed).")

        elif cmd == "exit":
            print("Bye!")
            break

        else:
            print("Unknown command. Try again.")

if __name__ == "__main__":
    main()
