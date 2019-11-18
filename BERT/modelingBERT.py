model = AdaptiveModel(
    language_model=language_model,
    prediction_heads=[ner_prediction_head],
    embeds_dropout_prob=EMBEDS_DROPOUT_PROB,
    lm_output_types=["per_token"],
    device=device)

optimizer, warmup_linear = initialize_optimizer(
    model=model,
    learning_rate=LEARNING_RATE,
    warmup_proportion=WARMUP_PROPORTION,
    n_batches=len(data_silo.loaders["train"]),
    n_epochs=N_EPOCHS)

trainer = Trainer(
    optimizer=optimizer,
    data_silo=data_silo,
    epochs=N_EPOCHS,
    n_gpu=N_GPU,
    warmup_linear=warmup_linear,
    device=device)

model = trainer.train(model)