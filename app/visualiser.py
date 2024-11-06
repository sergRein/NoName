from tabulate import tabulate
from colorama import Fore, Style, init

init(autoreset=True)

def show_menu():
    menu_data = [
        [f"{Fore.GREEN}help or menu{Style.RESET_ALL}", f"{Fore.GREEN}Show available commands{Style.RESET_ALL}"],
        [f"{Fore.GREEN}hello{Style.RESET_ALL}", f"{Fore.GREEN}Show hello message{Style.RESET_ALL}"],
        [f"{Fore.GREEN}all{Style.RESET_ALL}", f"{Fore.GREEN}Show all phones in address book{Style.RESET_ALL}"],
        [f"{Fore.GREEN}add [name] [phone]{Style.RESET_ALL}", f"{Fore.GREEN}Add new record{Style.RESET_ALL}"],
        [f"{Fore.GREEN}change [name] [old_phone] [new_phone]{Style.RESET_ALL}", f"{Fore.GREEN}Change phone number{Style.RESET_ALL}"],
        [f"{Fore.GREEN}phone [name]{Style.RESET_ALL}", f"{Fore.GREEN}Show phone for user with name{Style.RESET_ALL}"],
        [f"{Fore.GREEN}add-birthday [name] [date]{Style.RESET_ALL}", f"{Fore.GREEN}Add birthday for user{Style.RESET_ALL}"],
        [f"{Fore.GREEN}show-birthday [name]{Style.RESET_ALL}", f"{Fore.GREEN}Show birthday for user{Style.RESET_ALL}"],
        [f"{Fore.GREEN}birthdays ([period]){Style.RESET_ALL}", f"{Fore.GREEN}Show birthdays; default is next 7 days (options: 'next-week', 'next-month'){Style.RESET_ALL}"],
        [f"{Fore.GREEN}close or exit{Style.RESET_ALL}", f"{Fore.GREEN}Exit from program{Style.RESET_ALL}"]
    ]
    
    table = tabulate(menu_data, headers=[f"{Fore.GREEN}Command{Style.RESET_ALL}", f"{Fore.GREEN}Description{Style.RESET_ALL}"], tablefmt="grid")
    print(Style.BRIGHT + table)

