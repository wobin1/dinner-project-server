import typer
from rich import print
from rich.console import Console
from rich.table import Table
from rich.progress import track
import os

console= Console()

def create_folder(folder_name: str, file_content: str = ""):
    total = 0
    files = ['__init__.py', 'router.py', 'config.py', 'dependency.py', 'schemas.py', 'utils.py']
    try:
        # creating the folder
        os.makedirs('src\\modules\\'+folder_name, exist_ok=True)
        print(f"created folder with name {folder_name}")

        # creating the file
        for index, file in enumerate(files):
            file_path  = os.path.join('src\\modules\\'+folder_name, file)
            for value in track(range(100), description=f"creating {file} "):
                with open(file_path, 'w') as f:
                    f.write(file_content)
            print(f"[green]created {file}[/green]")
    except Exception as e:
        print(e)

def main(folder_name: str, file_content: str = ""):
    create_folder(folder_name, file_content)



if __name__ == '__main__':
    typer.run(main)