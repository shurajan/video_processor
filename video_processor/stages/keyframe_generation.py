from .base import ProcessingStage
import subprocess
import logging

logger = logging.getLogger(__name__)

class KeyframeGenerationStage(ProcessingStage):
    @property
    def name(self) -> str:
        return "Генерация ключевых кадров"

    def execute(self, video_info, context: dict) -> dict:
        for output_dir in context['output_dirs']:
            segments = output_dir / 'segments'
            keyframes = output_dir / 'keyframes'
            for segment in segments.glob('*.ts'):
                num = segment.stem
                out = keyframes / f"{num}.jpg"
                cmd = [
                    'ffmpeg', '-v', 'error', '-y', '-i', str(segment),
                    '-frames:v', '1', '-q:v', '2', str(out)
                ]
                try:
                    subprocess.run(cmd, check=True, capture_output=True)
                    logger.info(f"🖼️ Ключевой кадр {num}.jpg создан")
                except subprocess.CalledProcessError as e:
                    logger.warning(f"⚠️ Не удалось создать кадр для {segment}: {e}")
        return context
