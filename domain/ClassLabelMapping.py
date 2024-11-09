class ClassLabelMapping:
    MAPPING = {
        '人': 0,
        '工': 1,
        '十': 2,
        '上': 3,
        '下': 4,
        '王': 5,
        '一': 6,
        '大': 7,
        '小': 8,
        '火': 9,
    }
    REVERSE_MAPPING = {
        0: "人",
        1: "工",
        2: "十",
        3: "上",
        4: "下",
        5: "王",
        6: "一",
        7: "大",
        8: "小",
        9: "火"
    }

    @staticmethod
    def from_input_data(input_data):
        return ClassLabelMapping.MAPPING[input_data.label]

    @staticmethod
    def load_labels_from_file(file_path):
        label_mapping = {}
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    # Предполагается, что файл содержит метки в формате: "метка,число"
                    label, number = line.strip().split(',')
                    label_mapping[int(number)] = label
        except Exception as e:
            raise RuntimeError(f"Error loading labels from file: {e}")

        return label_mapping
