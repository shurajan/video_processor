from .base import ProcessingStage
import logging

logger = logging.getLogger(__name__)

class DirectoryPreparationStage(ProcessingStage):
    @property
    def name(self) -> str:
        return "Подготовка директорий"

    def execute(self, video_info, context: dict) -> dict:
        from pathlib import Path
        logger.info(f"📁 {self.name}")
        threshold = context.get('threshold', 5400)

        if video_info.duration <= threshold:
            output_dirs = [video_info.output_base]
        else:
            hours = max(1, int((video_info.duration / 3600) + 0.5))
            output_dirs = [
                video_info.basedir / f"{video_info.basename}_part_{i+1}"
                for i in range(hours)
            ]

        for output_dir in output_dirs:
            if output_dir.exists():
                raise Exception(f"Директория уже существует: {output_dir}")

        for output_dir in output_dirs:
            (output_dir / "segments").mkdir(parents=True, exist_ok=True)
            (output_dir / "keyframes").mkdir(parents=True, exist_ok=True)
            logger.info(f"📁 Создана: {output_dir}")

        context['output_dirs'] = output_dirs
        context['is_long_video'] = video_info.duration > threshold

        return context
