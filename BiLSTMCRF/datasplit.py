reviews_train, reviews_dev_test = train_test_split(reviews, test_size=0.3, random_state=42)
reviews_dev, reviews_test = train_test_split(reviews_dev_test, test_size = (1/3), random_state=42)
df_new_train = df_new[df_new['Review'].isin(reviews_train)]
df_new_dev = df_new[df_new['Review'].isin(reviews_dev)]
df_new_test = df_new[df_new['Review'].isin(reviews_test)]