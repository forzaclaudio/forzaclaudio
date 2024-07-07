#!/usr/bin/env python3

import click

from nano_vision import commands

@click.group()
def cli():
    pass

@cli.command()
@click.option('--source', help='Path to a video source. If empty, a live feed will be used.')
def capture_image(source):
    """Captures image from video or stream."""
    click.echo("Press q to stop playing and save the current image")
    try:
        commands.capture_image(source)
    except Exception as e:
        click.echo(click.style(str(e), fg="red"))

@cli.command()
@click.option('--source', help='Path to a video source. If empty, a live feed will be used.')
@click.option('--save_last_frame', default=False, help='Indicates if the last frame must be save as image.')
def extract_roi(source, save_last_frame):
    """Allows to click and retrieve the coordinates of a ROI."""
    click.echo("Press q to quit.")
    commands.extract_roi(source, save_last_frame)


@cli.command()
@click.option('--no_elapsed_time', default=False, help='Indicates that no elapsed time is added to the captured video.')
@click.option('--file-prefix', help='Prefix the saved filename with it.')
def capture_video(no_elapsed_time, file_prefix):
    """Capture video from stream."""
    click.echo("Press q to quit and save the current video.")
    commands.capture_video(no_elapsed_time=no_elapsed_time, file_prefix=file_prefix)

if __name__ == '__main__':
    cli()
