def word2idx(word):
  if word not in word_to_index:
    idx = word_to_index['unk']
  else:
    idx = word_to_index[word]
  return idx