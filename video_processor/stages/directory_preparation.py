from .base import ProcessingStage
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class DirectoryPreparationStage(ProcessingStage):
    @property
    def name(self) -> str:
        return "Подготовка директорий"

    def execute(self, video_info, context: dict) -> dict:
        logger.info(f"📁 {self.name}")

        output_dir = video_info.output_base

        if output_dir.exists():
            raise Exception(f"Директория уже существует: {output_dir}")

        (output_dir / "segments").mkdir(parents=True, exist_ok=True)
        (output_dir / "keyframes").mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 Создана: {output_dir}")

        context['output_dirs'] = [output_dir]
        return context