def pretrained_embedding_layer(word_to_vec_map, word_to_index):
  vocab_len = len(word_to_index) + 1
  emb_dimension = word_to_vec_map['gurke'].shape[0]
  emb_matrix = np.zeros((vocab_len, emb_dimension))
  for word, index in word_to_index.items():
    emb_matrix[index, :] = word_to_vec_map[str(word)]
 
  embedding_layer = Embedding(vocab_len, emb_dimension, trainable=False)
  embedding_layer.build((None,))
  embedding_layer.set_weights([emb_matrix])

  return embedding_layer