def get_labeled_sentences(number, annotations, relations):
    file_name_txt = '%s.txt' % number
    full_file_txt = os.path.abspath(os.path.join('data', file_name_txt))
    fhand_txt = open(full_file_txt, "r", encoding='utf-8')
    data = fhand_txt.read().replace('\n', ' ')
    data = ' '.join(data.split())
    doc = nlp(data)
    tokens = list()
    for token in doc:
        tokens.append(token.text)
    review = ['review%s' %number] * len(doc)
    bio_arr = ['O'] * len(doc)
    ann_text = ['O'] * len(doc)
    ann_ann = ['O'] * len(doc)
    ann_names = ['O'] * len(doc)
    ann_rel = ['O'] * len(doc)
    for ann in annotations:
        rngs = substring_range(data, ann[0])
        t1 = data[:rngs[0]]
        l1 = len(nlp(t1))
        between = len(nlp(ann[0]))
        bio_arr[l1] = 'B'
        ann_text[l1] = ann[0]
        ann_ann[l1] = ann[1]
        ann_names[l1] = ann[2]
        for rel in relations:
            if ann[2] == rel[0]:
                ann_rel[l1] = rel[1]
        for i in range(l1 + 1, l1 + between):
            bio_arr[i] = 'I'

    return review[1:], tokens[1:], bio_arr[1:], ann_text[1:], ann_ann[1:], ann_names[1:], ann_rel[1:]