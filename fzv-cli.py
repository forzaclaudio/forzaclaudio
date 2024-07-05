#!/usr/bin/env python3


from turtle import color
import click

from nano_vision import commands

@click.group()
def cli():
    pass

@cli.command()
@click.option('--source', help='Path to a video source. If empty, a live feed will be used.')
def image_capture(source):
    """Simple program that captures image from video."""
    click.echo("Press q to stop playing and save the current image")
    try:
        commands.image_capture(source)
    except Exception as e:
        click.echo(click.style(str(e), fg="red"))

if __name__ == '__main__':
    cli()
