#!/usr/bin/env python3

import click

from nano_vision import commands

@click.group()
def cli():
    pass

@cli.command()
@click.option('--source', help='Path to a video source. If empty, a live feed will be used.')
@click.option('--save_as', help='Path or name of file to save.')
def capture_image(source, save_as):
    """View video or stream and save image upon quiting."""
    click.echo("Press q to stop playing and save the current image")
    try:
        commands.capture_image(source, save_as)
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
    """View and capture video from stream."""
    click.echo("Press q to quit and save the current video.")
    commands.capture_video(no_elapsed_time=no_elapsed_time, file_prefix=file_prefix)

@cli.command()
@click.option('--training-dir', help='Directory with faces to learn.')
def learn_faces(training_dir):
    """
    Learn the faces from images in the given director.
    """
    commands.learn_faces(training_dir=training_dir)

if __name__ == '__main__':
    cli()
