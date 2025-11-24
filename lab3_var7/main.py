from image_processor import (
    parse_arguments,
    validate_arguments,
    load_image,
    convert_and_binarize,
    save_image
)


def main() -> None:

    args = parse_arguments()
    
    try:
        validate_arguments(args.input, args.threshold)

        original_img = load_image(args.input)
        
        height, width, channels = original_img.shape
        print(f"Размер: {width}x{height}, Каналы: {channels}")
        
        binary_img = convert_and_binarize(original_img, args.threshold)
        
        save_image(binary_img, args.output)
        print(f"Бинарное изображение успешно сохранено: {args.output}")
        
        print(f"Обработка завершена! Порог: {args.threshold}")
        
    except FileNotFoundError as e:
        print(f"Ошибка файла: {e}")
    except ValueError as e:
        print(f"Ошибка значения: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()