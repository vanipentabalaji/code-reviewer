import os
from rich.console import Console
from rich.panel import Panel
from rich.spinner import Spinner
from rich.live import Live
from client import review

console = Console()

def get_code_files():
    SKIP = {"venv", "__pycache__", ".git", "node_modules", ".env", "target", "build"}
    CODE_EXTENSIONS = {".py", ".js", ".ts", ".java", ".cpp", ".c", ".html", ".css", ".json"}
    
    files = []
    for root, dirs, filenames in os.walk("."):
        # Remove skipped folders so os.walk doesn't go into them
        dirs[:] = [d for d in dirs if d not in SKIP]
        
        for filename in sorted(filenames):
            if os.path.splitext(filename)[1] in CODE_EXTENSIONS:
                # Show relative path so user knows where file is
                relative_path = os.path.join(root, filename)
                files.append(relative_path)
    
    return files

def main():
    console.print(Panel(
        "[bold cyan]Welcome to Code Reviewer! 🤖[/bold cyan]\n"
        "[dim]Powered by Gemini + MCP[/dim]",
        border_style="cyan"
    ))

    files = get_code_files()

    if not files:
        console.print("\n[red]No code files found in current directory.[/red]")
        return

    console.print("\n[bold]📁 Files available for review:\n[/bold]")
    for i, file in enumerate(files, start=1):
        console.print(f"  [cyan][{i}][/cyan] {file}")

    console.print()
    choice = console.input("[bold green]Enter file number:[/bold green] ")

    if not choice.isdigit():
        console.print("\n[red]Please enter a valid number.[/red]")
        return

    index = int(choice) - 1

    if index < 0 or index >= len(files):
        console.print("\n[red]Number out of range.[/red]")
        return

    selected_file = files[index]
    console.print(f"\n[green]✅ Selected:[/green] {selected_file}")

    with Live(Spinner("dots", text="[cyan]Reviewing your code...[/cyan]"), refresh_per_second=10):
        result = review(selected_file)

    console.print()
    console.print(Panel(
        result,
        title=f"[bold cyan]📋 Code Review — {selected_file}[/bold cyan]",
        border_style="cyan"
    ))

if __name__ == "__main__":
    main()