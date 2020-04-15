from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.files import write_file
from datetime import date
import pathlib
import os
import colorama
from colorama import Fore, Style
from tqdm import tqdm
from pyfiglet import Figlet


nr = InitNornir(config_file="config.yaml")

clear_commands = "clear"
os.system(clear_commands)

sub_fig = Figlet(font='roman')
print(sub_fig.renderText('IPvZero'))

def archive_telemetry(task, get_bar):
    commands = ["show run", "show cdp neighbor detail", "show version",
    "show clock", "show logging", "show ip ospf int brief",
    "show ip ospf database", "show ip bgp neighbor"]
    for cmd in commands:
        name = str(cmd)
        folder = name.replace(" ", "-")
        config_dir = "config-archive"
        date_dir = config_dir + "/" + str(date.today())
        command_dir = date_dir + "/" + folder
        pathlib.Path(config_dir).mkdir(exist_ok=True)
        pathlib.Path(date_dir).mkdir(exist_ok=True)
        pathlib.Path(command_dir).mkdir(exist_ok=True)
        r = task.run(task=send_command, command=cmd)
        task.run(
            task=write_file,
            content=r.result,
            filename=f"" + str(command_dir) + "/" + task.host.name + ".txt",)

    get_bar.update()
    tqdm.write(Fore.YELLOW + "Gathering network statistics for " + Fore.MAGENTA + Style.BRIGHT + f"{task.host}\n" )


with tqdm(
    total=len(nr.inventory.hosts), desc="Creating Archive",
) as get_bar:
    nr.run(
        task=archive_telemetry,
        get_bar=get_bar,
    )

print(Fore.GREEN + "Archive Created")
