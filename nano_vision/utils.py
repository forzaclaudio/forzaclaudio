from datetime import datetime

def _to_string(ts):
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')

def generate_filename(prefix=None, width=None, height=None, timestamp=None, suffix="mp4"):
    filename = ""
    if prefix:
        filename += prefix
    else:
        filename += "video"
    if width and height:
        filename += "-{0}x{1}".format(width, height)
    if timestamp:
        filename += "-{0}".format(_to_string(timestamp))
    filename += ".{0}".format(suffix)
    return filename