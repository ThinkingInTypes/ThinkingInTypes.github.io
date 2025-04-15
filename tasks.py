# tasks.py
"""
'Invoke' command file.
"""
import sys
from pathlib import Path

from invoke import Collection, task
from pybooktools.invoke_tasks import prettier, rewrite_with_semantic_breaks
from pybooktools.md_cleaner import clean_markdown
from rich.console import Console
from rich.prompt import Confirm

WIDTH = 60  # Width for code listings and comments

markdown_chapters_path = Path("C:/git/ThinkingInTypes.github.io/Chapters")

console = Console()


def confirm(message: str, default: bool = True) -> None:
    if not Confirm.ask(
        f"[yellow]{message}[/yellow]",
        default=default,
    ):
        console.print("[red]Cancelled by user.[/red]")
        sys.exit(1)


@task(default=True)
def z(ctx) -> None:
    """
    List available tasks.
    """
    ctx.run("invoke -l")


@task
def sembr(ctx, chapter: Path):
    """
    Adds semantic breaks to the specified chapter.
    """
    _ = ctx
    if not isinstance(chapter, Path):
        chapter = Path(chapter)
    rewrite_with_semantic_breaks(chapter)


@task
def cleanmd(ctx, chapter: Path):
    """
    clean markdown files
    """
    _ = ctx
    if not isinstance(chapter, Path):
        chapter = Path(chapter)
    markdown = chapter.read_text(encoding="utf-8")
    cleaned_markdown = clean_markdown(markdown)
    chapter.write_text(cleaned_markdown, encoding="utf-8")


namespace = Collection(z, sembr, prettier, cleanmd)
