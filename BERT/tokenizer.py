tokenizer = BertTokenizer.from_pretrained(
	pretrained_model_name_or_path="bert-base-german-cased",
	do_lower_case=False)

ner_processor = NERProcessor(
	tokenizer=tokenizer, 
	max_seq_len=512,
	train_filename='train.txt',
	dev_filename='dev.txt',
	test_filename='test.txt')

ner_labels = ['B-B-Claim', 'B-I-Claim', 'B-B-Premise', 'B-I-Premise', 'B-O', 'X', '[PAD]']
ner_processor.add_task("ner", "seq_f1", ner_labels)

data_silo = DataSilo(
    processor=ner_processor,
    batch_size=BATCH_SIZE)