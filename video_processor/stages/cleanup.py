from .base import ProcessingStage
import logging

logger = logging.getLogger(__name__)

class CleanupStage(ProcessingStage):
    @property
    def name(self) -> str:
        return "Очистка"

    def execute(self, video_info, context: dict) -> dict:
        if context.get('keep_original', False):
            logger.info(f"🔒 Исходный файл сохранен: {video_info.input_path}")
        else:
            try:
                video_info.input_path.unlink()
                logger.info(f"🗑️ Удален исходный файл: {video_info.input_path}")
            except OSError as e:
                logger.warning(f"⚠️ Не удалось удалить файл: {e}")
        return context
