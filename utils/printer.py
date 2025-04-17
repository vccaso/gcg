import re
from config import __version__, __app_name__, __workflow_path__, debug


class Printer:
   GREEN = "\033[92m"
   YELLOW = "\033[93m"
   RED = "\033[91m"
   RESET = "\033[0m"
   WHITE = "\033[97m"
   BLUE = "\033[94m"
   MAGENTA = "\033[95m"
   CYAN = "\033[96m"


   @staticmethod
   def message(message: str):
       """Print message in green; highlight <strong> tags in yellow."""
       def highlight(match):
           return f"{Printer.YELLOW}{match.group(1)}{Printer.WHITE}"


       formatted_message = re.sub(r'<strong>(.*?)</strong>', highlight, message)
       print(f"{Printer.WHITE}{formatted_message}{Printer.RESET}")


   @staticmethod
   def success(message: str):
       """Print message in green; highlight <strong> tags in yellow."""
       if debug:
            def highlight(match):
                return f"{Printer.YELLOW}{match.group(1)}{Printer.GREEN}"


            formatted_message = re.sub(r'<strong>(.*?)</strong>', highlight, message)
            print(f"{Printer.GREEN}{formatted_message}{Printer.RESET}")


   @staticmethod
   def error(message: str):
       def highlight(match):
           return f"{Printer.YELLOW}{match.group(1)}{Printer.RED}"


       formatted_message = re.sub(r'<strong>(.*?)</strong>', highlight, message)
       print(f"{Printer.RED}{formatted_message}{Printer.RESET}")



