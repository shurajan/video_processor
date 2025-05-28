from .base import ProcessingStage
import os
import cv2
import logging
from nudenet import NudeDetector

logger = logging.getLogger(__name__)

CONFIDENCE_THRESHOLD = 0.5
NSFW_CLASSES_PRIORITY = [
    "FEMALE_BREAST_EXPOSED",
    "ANUS_EXPOSED",
    "FEMALE_GENITALIA_EXPOSED"
]
NSFW_CLASS_TO_PRIORITY = {cls: i for i, cls in enumerate(NSFW_CLASSES_PRIORITY)}


class NSFWScanStage(ProcessingStage):
    @property
    def name(self) -> str:
        return "NSFW-анализ .ts сегментов в /segments"

    def execute(self, video_info, context: dict) -> dict:
        detector = NudeDetector()

        for output_dir in context.get("output_dirs", []):
            segments_dir = output_dir / "segments"
            if not segments_dir.is_dir():
                logger.warning(f"📂 Каталог 'segments/' не найден в: {output_dir}")
                continue

            nsfw_dir = output_dir / "nsfw"
            found_nsfw = False

            for fname in sorted(os.listdir(segments_dir)):
                if not fname.endswith(".ts"):
                    continue

                ts_path = segments_dir / fname
                logger.info(f"🔍 Сканирование {ts_path}")
                nsfw_frame = self.analyze_ts_file(ts_path, detector)

                if nsfw_frame is not None:
                    if not found_nsfw:
                        nsfw_dir.mkdir(exist_ok=True)
                        found_nsfw = True

                    output_path = nsfw_dir / f"{ts_path.stem}.jpg"
                    cv2.imwrite(str(output_path), nsfw_frame)
                    logger.info(f"💥 NSFW кадр сохранён: {output_path}")

            if not found_nsfw:
                logger.info(f"✅ NSFW контент не обнаружен в: {output_dir}")

        return context

    def analyze_ts_file(self, ts_path, detector):
        cap = cv2.VideoCapture(str(ts_path))
        if not cap.isOpened():
            logger.warning(f"⚠️ Не удалось открыть видео: {ts_path}")
            return None

        best_priority = -1
        best_score = 0.0
        best_frame = None
        best_results = []

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 25
        frame_idx = 0

        while frame_idx < total_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            if not ret:
                break

            success, encoded_image = cv2.imencode(".jpg", frame)
            if not success:
                frame_idx += int(fps)
                continue

            results = detector.detect(encoded_image.tobytes())

            filtered = [
                r for r in results
                if r["class"] in NSFW_CLASS_TO_PRIORITY and r["score"] >= CONFIDENCE_THRESHOLD
            ]

            if filtered:
                top = max(filtered, key=lambda r: (NSFW_CLASS_TO_PRIORITY[r["class"]], r["score"]))
                priority = NSFW_CLASS_TO_PRIORITY[top["class"]]

                should_replace = (
                    priority > best_priority or
                    (priority == best_priority and top["score"] > best_score)
                )

                if should_replace:
                    best_priority = priority
                    best_score = top["score"]
                    best_frame = frame.copy()
                    best_results = filtered

            frame_idx += int(fps)

        cap.release()

        if best_frame is not None:
            for r in best_results:
                x, y, w, h = r["box"]
                x1, y1 = int(x), int(y)
                x2, y2 = x1 + int(w), y1 + int(h)
                label = f"{r['class']} {r['score']:.2f}"
                cv2.rectangle(best_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(best_frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            return best_frame

        return None