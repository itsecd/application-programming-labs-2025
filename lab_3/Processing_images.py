import os
from ImagePathIterator import ImagePathIterator
from Add_a_frame import frame_adder


def process_all_images(input_folder: str, output_folder: str) -> None:
    """Обрабатывает все изображения в папке"""
    print(f"Исходные изображения: {input_folder}")
    print(f"Сохранение результатов: {output_folder}")

    if not os.path.exists(output_folder):
        try:
            os.mkdir(output_folder)
            print(f"Создана папка: {output_folder}")
        except OSError as e:
            print(f"Ошибка при создании папки: {e}")
            return

    try:
        image_iterator = ImagePathIterator(input_folder)
        total_images = len(image_iterator)
        
        if total_images == 0:
            print("В папке не найдено изображений")
            return
        
        print(f"Найдено изображений: {total_images}")
        print("Закройте окно matplotlib чтобы продолжить обработку следующего изображения")
        print()
        
        successful = 0
        failed = 0
        
        counter = 1
        for image_path in image_iterator:
            success = frame_adder(image_path, output_folder, counter)
            if success:
                successful += 1
            else:
                failed += 1
            
            counter += 1 
            print("-" * 30)  
        
        print("=" * 50)
        print(f"Успешно: {successful} | Ошибок: {failed} | Всего: {total_images}")
        print(f"Результаты в: {output_folder}")

    except Exception as e:
        print(f"Ошибка: {e}")