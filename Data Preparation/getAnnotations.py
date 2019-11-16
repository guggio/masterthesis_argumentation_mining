def get_annotations(number):
    file_name_ann = '%s.ann' %number
    full_file_ann = os.path.abspath(os.path.join('data', file_name_ann))
    fhand_ann = open(full_file_ann, "r", encoding='utf-8')
    annotation_text = dict()
    relations = dict()
    for line in fhand_ann:
        line = line.rstrip()
        line = line.split()
        if line[0].startswith('T'):
            annotation_text[line[0]] = [' '.join(line[4:]), line[1], line[0], int(line[2])]
        else:
            relations[line[0]] = [line[2][5:], line[3][5:]]

    return annotation_text, relations