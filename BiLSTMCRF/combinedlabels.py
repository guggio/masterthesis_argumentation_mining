z = 'O'
combined_labels = list()
for i in range(len(df)):
	if df['BIO'].iloc[i] == 'B':
		z = df['Ann_Ann'].iloc[i]
		combined_labels.append('B-' + z)
	elif df['BIO'].iloc[i] == 'I':
		combined_labels.append('I-' + z)
	else:
		z = 'O'
		combined_labels.append(z)

df['combined_labels'] = combined_labels