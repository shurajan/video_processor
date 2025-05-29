from .stages import (
    ValidationStage, DirectoryPreparationStage, HLSConversionStage,
    KeyframeGenerationStage, CleanupStage
)
from .stages.fix_corrupted import FixCorruptedStage
from .stages.nsfw_scan_stage import NSFWScanStage
from .videoinfo import VideoInfo, VideoProcessorError
import logging
import sys
from typing import List, Optional

logger = logging.getLogger(__name__)

class VideoProcessor:
    def __init__(self):
        self.stages: List = []
        self._setup_default_stages()

    def _setup_default_stages(self):
        self.stages = [
            FixCorruptedStage(),
            ValidationStage(),
            DirectoryPreparationStage(),
            HLSConversionStage(),
            KeyframeGenerationStage(),
            NSFWScanStage(),
            CleanupStage(),
        ]

    def add_stage(self, stage, position: Optional[int] = None):
        if position is None:
            self.stages.append(stage)
        else:
            self.stages.insert(position, stage)

    def remove_stage(self, stage_class: type):
        self.stages = [s for s in self.stages if not isinstance(s, stage_class)]

    def process(self, input_path: str, keep_original: bool = False) -> dict:
        try:
            video_info = VideoInfo(input_path)
            context = {
                'keep_original': keep_original
            }

            logger.info(f"🚀 Начало обработки: {input_path}")

            for stage in self.stages:
                context = stage.execute(video_info, context)

            logger.info("🎉 Обработка завершена успешно!")
            return context

        except VideoProcessorError as e:
            logger.error(f"❌ Ошибка: {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            logger.error("❌ Обработка прервана пользователем")
            sys.exit(1)
        except Exception as e:
            logger.error(f"❌ Неожиданная ошибка: {e}")
            sys.exit(1)
