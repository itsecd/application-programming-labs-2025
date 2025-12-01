import os
from ImagePathIterator import ImagePathIterator
from Add_a_frame import frame_adder


def process_all_images(input_folder: str, output_folder: str, frame_width: int, frame_color: tuple) -> None:
    """Обрабатывает все изображения в папке"""
    if not os.path.exists(output_folder):
        try:
            os.mkdir(output_folder)
        except OSError:
            return

    try:
        image_iterator = ImagePathIterator(input_folder)
        total_images = len(image_iterator)
        
        if total_images == 0:
            return
        
        successful = 0
        failed = 0
        
        counter = 1
        for image_path in image_iterator:
            success = frame_adder(image_path, output_folder, counter, frame_width, frame_color)
            if success:
                successful += 1
            else:
                failed += 1
            
            counter += 1
        
        print("=" * 50)
        print(f"Успешно: {successful} | Ошибок: {failed} | Всего: {total_images}")
        print(f"Результаты в: {output_folder}")

    except Exception:
        pass