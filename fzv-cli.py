#!/usr/bin/env python3


from turtle import color
import click

from nano_vision import commands

@click.group()
def cli():
    pass

@cli.command()
@click.option('--source', help='Path to a video source. If empty, a live feed will be used.')
def capture_image(source):
    """Simple program that captures image from video or stream."""
    click.echo("Press q to stop playing and save the current image")
    try:
        commands.capture_image(source)
    except Exception as e:
        click.echo(click.style(str(e), fg="red"))

@cli.command()
@click.option('--source', help='Path to a video source. If empty, a live feed will be used.')
@click.option('--save_last_frame', default=False, help='Indicates if the last frame must be save as image.')
def extract_roi(source, save_last_frame):
    """Simple program that extracts coordinates of ROI."""
    click.echo("Press q to quit.")
    commands.extract_roi(source, save_last_frame)

if __name__ == '__main__':
    cli()
