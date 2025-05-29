from .base import ProcessingStage
import subprocess
import logging

logger = logging.getLogger(__name__)

class HLSConversionStage(ProcessingStage):
    @property
    def name(self) -> str:
        return "Конвертация HLS"

    def execute(self, video_info, context: dict) -> dict:
        output_dirs = context['output_dirs']
        self._convert_single(video_info, output_dirs[0])
        return context

    def _convert_single(self, video_info, output_dir):
        logger.info(f"🎬 Создание плейлиста в {output_dir}")

        cmd = [
            'ffmpeg', '-i', str(video_info.input_path),
            '-c:v', 'copy', '-c:a', 'copy',
            '-hls_time', '5',
            '-hls_segment_type', 'mpegts',
            '-hls_flags', 'independent_segments',
            '-hls_segment_filename', str(output_dir / 'segments' / '%d.ts'),
            '-hls_base_url', './segments/',
            '-hls_list_size', '0',
            '-f', 'hls', str(output_dir / 'playlist.m3u8')
        ]

        self._run_ffmpeg(cmd)

    def _run_ffmpeg(self, cmd):
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Ошибка ffmpeg: {e.stderr.decode()}")
