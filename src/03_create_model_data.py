miport pandas as pd
import numpy as np
import re


# 1 READING DATA

###
# 1.1 Pfam data

# Pfam proteins associated with nucleus terms and membrane terms in keyword search
df_pfam_locations = pd.read_csv('../input/pfam_nucleus_membrane_data.csv')

# The searched terms
nucleus_terms = ['chromossome', 'chromatin', 'nucleus', 'nucleic']
membrane_terms = ['membrane', 'cytoplasm', 'cytoskeleton', 'cytosol']

# Add variable to identify if is a nucleus or membrane term
df_pfam_locations['flag_nucleus'] = np.where(df_pfam_locations['keyword'].isin(nucleus_terms), 1, 0)
df_pfam_locations['flag_membrane'] = np.where(df_pfam_locations['keyword'].isin(membrane_terms), 1, 0)


# The Pfam keyword search find the same accession in different terms
# so I will group these values
df_pfam_locations = df_pfam_locations.groupby('accession')[['flag_nucleus', 'flag_membrane']].max().reset_index()

###
# 1.2 HMM output DataFrame

df_hmm = pd.read_csv('../output/df_t_cruzi_hmm.csv', low_memory=False)

# Remove any character after dot in accession ('.')
df_hmm.accession = df_hmm.accession.apply(lambda x: re.sub(r'\..*', '', x.strip()))
# Strip whitespace from target, query name and score
df_hmm.target_name = df_hmm.target_name.apply(lambda x: x.strip())
df_hmm.query_name = df_hmm.query_name.apply(lambda x: x.strip())



###
# 1.3 Swissprot data
df_swissprot = pd.read_csv('../output/df_swiss_prot_t_cruzi.csv')
df_swissprot.drop('Unnamed: 0', axis=1, inplace=True)
df_swissprot.dropna(inplace=True)

# Transforming variables
df_swissprot['accession_2'] = df_swissprot.iteration_query_def.str.split('|', expand=True).iloc[:,1]
df_swissprot['query_name'] = df_swissprot.query_id.str.split('|', expand=True).iloc[:,0]
df_swissprot['query_name'] = df_swissprot.query_name.apply(lambda x: str(x).strip())


# 2 JOIN DATA

###
# 2.1 Join T. Cruzi hmm on Swissprot data
df_model = df_hmm[['accession', 'query_name', 'score']].merge(df_swissprot[['query_name', 'accession_2']], how='left')

###
# 2.2 Add Pfam keywords
df_model = df_model.merge(df_pfam_locations, how='left')

# Define train and predictions dataframe
df_train = df_model[df_model.accession_2.notna()].reset_index(drop=True)
df_pred = df_model[df_model.accession_2.isna()].reset_index(drop=True)

# Add features
df_train['score_nucleus'] = np.where(df_train.flag_nucleus.isna(), df_train.score, df_train.flag_nucleus*df_train.score)
df_train['score_membrane'] = np.where(df_train.flag_membrane.isna(), df_train.score, df_train.flag_membrane*df_train.score)

df_pred['score_nucleus'] = np.where(df_pred.flag_nucleus.isna(), df_pred.score, df_pred.flag_nucleus*df_pred.score)
df_pred['score_membrane'] = np.where(df_pred.flag_membrane.isna(), df_pred.score, df_pred.flag_membrane*df_pred.score)

df_train = df_train.groupby('query_name')[['score_nucleus', 'score_membrane']].sum().reset_index()
df_pred = df_pred.groupby('query_name')[['score_nucleus', 'score_membrane']].sum().reset_index()

# Add target variable
df_train['classification'] = np.where(df_train.score_nucleus>df_train.score_membrane, 1, 0)
df_train.loc[df_train.score_nucleus==df_train.score_membrane, 'classification'] = 'draw'

# Save
df_train.to_csv('../output/df_train.csv', index=False)
df_pred.to_csv('../output/df_pred.csv', index=False)