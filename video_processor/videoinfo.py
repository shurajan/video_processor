import subprocess
from pathlib import Path

class VideoProcessorError(Exception):
    pass

class VideoInfo:
    def __init__(self, input_path: str):
        self.input_path = Path(input_path)
        self.basename = self.input_path.stem
        self.basedir = self.input_path.parent
        self.output_base = self.basedir / self.basename
        self.duration = self._get_duration()

    def _get_duration(self) -> int:
        try:
            cmd = [
                'ffprobe', '-v', 'error', '-select_streams', 'v:0',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                str(self.input_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return int(float(result.stdout.strip()))
        except (subprocess.CalledProcessError, ValueError) as e:
            raise VideoProcessorError(f"Не удалось получить длительность видео: {e}")
