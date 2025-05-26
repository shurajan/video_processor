from .base import ProcessingStage
import subprocess
import logging

logger = logging.getLogger(__name__)

class FixCorruptedStage(ProcessingStage):
    @property
    def name(self) -> str:
        return "Фиксация временных меток .ts файла"

    def execute(self, video_info, context: dict) -> dict:
        input_path = video_info.input_path
        fixed_path = input_path.with_name(f"{input_path.stem}_fixed{input_path.suffix}")

        logger.info(f"🛠️ {self.name}: принудительное исправление временных меток")

        cmd = [
            "ffmpeg", "-y",
            "-fflags", "+genpts",
            "-i", str(input_path),
            "-c:v", "copy", "-c:a", "copy",
            str(fixed_path)
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Ошибка при фиксации .ts файла: {e.stderr.decode()}")

        try:
            input_path.unlink()
            fixed_path.rename(input_path)
            logger.info(f"✅ Фиксированный файл заменил оригинал: {input_path}")
        except Exception as e:
            raise Exception(f"Ошибка при замене оригинального файла: {e}")

        return context