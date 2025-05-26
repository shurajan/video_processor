from .base import ProcessingStage
import subprocess
import logging

logger = logging.getLogger(__name__)

class HLSConversionStage(ProcessingStage):
    @property
    def name(self) -> str:
        return "Конвертация HLS"

    def execute(self, video_info, context: dict) -> dict:
        from pathlib import Path
        output_dirs = context['output_dirs']
        is_long_video = context['is_long_video']

        if not is_long_video:
            self._convert_single(video_info, output_dirs[0])
        else:
            self._convert_segments(video_info, output_dirs)

        return context

    def _convert_single(self, video_info, output_dir):
        logger.info(f"🎬 Короткое видео, создание плейлиста в {output_dir}")

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

    def _convert_segments(self, video_info, output_dirs):
        hours = len(output_dirs)
        segment_duration = video_info.duration // hours

        for i, output_dir in enumerate(output_dirs):
            start = i * segment_duration
            cmd = [
                'ffmpeg', '-ss', str(start), '-i', str(video_info.input_path),
                '-t', str(segment_duration),
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
