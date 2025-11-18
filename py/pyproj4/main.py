import cv2

import dfhelp

def main():
    try:
        parser = dfhelp.parsing()
        args = parser.parse_args()

        dfhelp.csv_check(args.annotation, args.dataframe_paths)

        data = dfhelp.create_data(args.annotation)

        absolute_paths = data['Абсолютеный путь'].tolist()

        data['Ширина'] = dfhelp.get_widths(absolute_paths)

        sorted_d = data.sort_values("Ширина", ascending=False)  # уже существует функция сортировки
        filtered_d = dfhelp.filter_data(data, 500, True)

        data.to_csv(args.dataframe_paths[0], index=True)
        sorted_d.to_csv(args.dataframe_paths[1], index=True)
        filtered_d.to_csv(args.dataframe_paths[2], index=True)

        dfhelp.install_graphs(data, args.graph_paths[0])
        dfhelp.install_graphs(sorted_d, args.graph_paths[1])
        dfhelp.install_graphs(filtered_d, args.graph_paths[2])

    except ValueError as e:
        print(e)
    except cv2.error as e:
        print(e)


if __name__ == "__main__":
    main()