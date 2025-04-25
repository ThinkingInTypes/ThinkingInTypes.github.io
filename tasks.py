# tasks.py
"""
'Invoke' command file.
"""
import sys
from pathlib import Path
from typing import Literal

from invoke import Collection, task
from pybooktools.invoke_tasks import prettier, rewrite_with_semantic_breaks
from pybooktools.md_cleaner import clean_ai_generated_markdown
from pybooktools.pymarkdown_validator.validate import validate_markdown_directory
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
def validatemd(ctx, verbose: Literal["verbose", "quiet"] = "quiet"):
    """
    Validate all Markdown files in the directory
    """
    _ = ctx
    validate_markdown_directory(markdown_chapters_path, verbose)


@task
def clean_ai_generated_md(ctx, chapter: Path):
    """
    clean markdown files
    """
    _ = ctx
    if not isinstance(chapter, Path):
        chapter = Path(chapter)
    markdown = chapter.read_text(encoding="utf-8")
    cleaned_markdown = clean_ai_generated_markdown(markdown)
    chapter.write_text(cleaned_markdown, encoding="utf-8")


namespace = Collection(z, sembr, prettier, clean_ai_generated_md, validatemd)
