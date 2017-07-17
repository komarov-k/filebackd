import click
import datetime
import os
import shutil
import time
import watchdog
from watchdog.events import *
from watchdog.observers.polling import PollingObserver

class FBDSystemEventHandler(FileSystemEventHandler):
    def __init__(self, source_path, target_path):
        self._source_path = os.path.abspath(source_path)
        self._target_path = os.path.abspath(target_path)

    def _mkdir_p(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def _backup(self, file_path):
        # Get absolute path of source file
        source_file_abs_path = os.path.abspath(file_path)
        # Avoid backing up backup files...
        if source_file_abs_path.startswith(self._target_path):
            return
        # Create absolute path of target file
        target_file_abs_path = source_file_abs_path.replace(self._source_path,
                                                            self._target_path)

        # Create target directory
        self._mkdir_p(os.path.dirname(target_file_abs_path))

        # Create time stamp for current time
        time_stamp = datetime.datetime.fromtimestamp(time.time())
        # Append time stamp to target file name
        target_file_abs_path += '.' + time_stamp.strftime('%Y-%m-%d %H:%M:%S')

        # Copy source file into target file...
        shutil.copyfile(source_file_abs_path, target_file_abs_path)
        shutil.copymode(source_file_abs_path, target_file_abs_path)
        shutil.copystat(source_file_abs_path, target_file_abs_path)

    def on_created(self, event):
        if isinstance(event, FileCreatedEvent):
            self._backup(event.src_path)

    def on_modified(self, event):
        if isinstance(event, FileModifiedEvent):
            self._backup(event.src_path)

    def on_moved(self, event):
        if isinstance(event, FileModifiedEvent):
            self._backup(event.dest_path)

@click.command()
@click.argument('source', type=click.Path(exists=True))
@click.argument('target', type=click.Path(exists=False))
def cli(source, target):
    """
    File backup daemon CLI
    """

    observer = PollingObserver()

    handler = FBDSystemEventHandler(source, target)
    
    observer.schedule(handler, source, recursive=True)
    
    observer.start()

    while True: 
        time.sleep(60)
