from .base import ProcessingStage
import logging

logger = logging.getLogger(__name__)

class ValidationStage(ProcessingStage):
    @property
    def name(self) -> str:
        return "Валидация"

    def execute(self, video_info, context: dict) -> dict:
        logger.info(f"🔍 {self.name}: проверка входного файла")

        if not video_info.input_path.exists():
            raise Exception(f"Файл не найден: {video_info.input_path}")

        if video_info.input_path.suffix.lower() != '.ts':
            raise Exception("Поддерживаются только .ts файлы")

        logger.info(f"✅ Файл валиден: {video_info.input_path}")
        logger.info(f"📊 Длительность: {video_info.duration} сек")

        return context
