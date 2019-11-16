import os
import spacy
nlp = spacy.load("de_core_news_sm")
import pandas as pd
import re
import time
import string
punctuations = string.punctuation
import collections

def takeFourth(elem):
    return elem[3]

def substring_range(s, substring):
    for i in re.finditer(re.escape(substring), s):
        return (int(i.start()), int(i.end()))

def get_annotations(number):
    file_name_ann = '%s.ann' %number
    full_file_ann = os.path.abspath(os.path.join('data', file_name_ann))

    fhand_ann = open(full_file_ann, "r", encoding='utf-8')
    annotation_text = dict()
    relations = dict()
    lines = list()
    for line in fhand_ann:
        line = line.rstrip()
        line = line.split()
        if line[0].startswith('T'):
            annotation_text[line[0]] = [' '.join(line[4:]), line[1], line[0], int(line[2])]
        else:
            relations[line[0]] = [line[2][5:], line[3][5:]]

    return annotation_text, relations

def get_labeled_sentences(number, annotations, relations):

    file_name_txt = '%s.txt' % number
    full_file_txt = os.path.abspath(os.path.join('data', file_name_txt))
    fhand_txt = open(full_file_txt, "r", encoding='utf-8')

    #Preparations of full_text
    data = fhand_txt.read().replace('\n', ' ')
    data = ' '.join(data.split())

    for ann in annotations:
        rngs = substring_range(data, ann[0])
        part_before = data[:rngs[0]]
        part_after = data[rngs[1]:]
        data = part_before + ' ' + ann[0] + ' ' + part_after

    data = ' '.join(data.split())
    doc = nlp(data)
    tokens = list()
    pos_tags = list()
    for token in doc:
        tokens.append(token.text)
        pos_tags.append(token.pos_)
    review = ['review%s' %number] * len(doc)
    token_arr = ['O'] * len(doc)

    ann_text = ['O'] * len(doc)
    ann_ann = ['O'] * len(doc)
    ann_names = ['O'] * len(doc)
    ann_rel = ['O'] * len(doc)

    for ann in annotations:
        rngs = substring_range(data, ann[0])
        t1 = data[:rngs[0]]
        l1 = len(nlp(t1))
        between = len(nlp(ann[0]))
        token_arr[l1] = 'B'
        ann_text[l1] = ann[0]
        ann_ann[l1] = ann[1]
        ann_names[l1] = ann[2]
        for rel in relations:
            if ann[2] == rel[0]:
                ann_rel[l1] = rel[1]
        for i in range(l1 + 1, l1 + between):
            token_arr[i] = 'I'

    return review[1:], tokens[1:], pos_tags[1:], token_arr[1:], ann_text[1:], ann_ann[1:], ann_names[1:], ann_rel[1:]

reviews = list()
start = time.time()
#for number in range(9,11):
for number in range(4842):

    try:
        annotation_text, relations = get_annotations(number)
        annotations = list(annotation_text.values())
        annotations.sort(key=lambda x: x[3])
        relations_list = list(relations.values())
        review, tokens, pos_tags, token_arr, ann_text, ann_ann, ann_names, ann_rel = get_labeled_sentences(number, annotations, relations_list)
        d = {'Review': review, 'Tokens': tokens, 'POS': pos_tags, 'BIO': token_arr, 'Ann_Text': ann_text,
             'Ann_Ann': ann_ann, 'Ann_Names': ann_names, 'Ann_Rel': ann_rel}
        df_review = pd.DataFrame(d)
        reviews.append(df_review)

    except:
        continue

df = pd.concat(reviews)

pd.set_option('display.max_columns', 30)
#print(df)

end = time.time()
print('total time:', (end - start))


#df.to_csv("check_v10.csv")
df.to_csv("full_annotations_v10.csv")



