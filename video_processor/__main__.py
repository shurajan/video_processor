import argparse
import logging

parser = argparse.ArgumentParser(
    description="Конвертация TS видео в HLS плейлисты"
)
parser.add_argument('input', help='Входной .ts файл')

parser.add_argument(
    '--keep-original', '-k', action='store_true',
    help='Сохранить исходный файл'
)
parser.add_argument(
    '--verbose', '-v', action='store_true',
    help='Подробный вывод'
)

args = parser.parse_args()

# Устанавливаем логирование до импорта обработчика
logging.basicConfig(
    level=logging.DEBUG if args.verbose else logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler()]
)

from video_processor.processor import VideoProcessor

def main():
    processor = VideoProcessor()
    processor.process(args.input, keep_original=args.keep_original)

if __name__ == '__main__':
    main()