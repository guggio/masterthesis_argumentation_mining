def write_inputfiles_txt(df, reviews, part):
    f = open('{}.txt'.format(part[r]), 'w+')
    for rev in reviews:
      df_relevant = df[df['Review'] == rev]
      for i in range(len(df_relevant)):
        f.write(str(df_relevant['Tokens'].iloc[i]) + '\t' + str(df_relevant['combined_labels'].iloc[i]))
        f.write('\n')
      f.write('\n')
    f.close()