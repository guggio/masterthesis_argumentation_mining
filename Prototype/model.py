def model(input_shape=(maxLen, ), word_to_vec_map=word_to_vec_map, word_to_index=word_to_index):
  review_indices = Input(shape = input_shape, dtype='int32')
  embedding_layer = pretrained_embedding_layer(word_to_vec_map, word_to_index)
  embeddings = embedding_layer(review_indices)
  X = Bidirectional(LSTM(units=hidden_units, return_sequences=True, recurrent_dropout=dropout))(embeddings)
  X = TimeDistributed(Dense(units=hidden_units, activation="relu"))(X)
  crf = CRF(n_labels)
  out = crf(X)
  model = Model(inputs=review_indices, outputs=out)
  model.compile(optimizer=optimizer, loss=crf.loss_function, metrics=[crf.accuracy])

  return model