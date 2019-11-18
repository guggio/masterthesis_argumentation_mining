z='O'
combined_labels = list()
for i in range(len(df_new)):
  if df_new['BIO'].iloc[i] == 'B':
    z = df_new['Ann_Ann'].iloc[i]
    combined_labels.append('B-B' + z)
  elif df_new['BIO'].iloc[i] == 'I':
    combined_labels.append('B-I' + z)
  else:
    z = 'O'
    combined_labels.append('B-' + z)

df_new['combined_labels'] = combined_labels