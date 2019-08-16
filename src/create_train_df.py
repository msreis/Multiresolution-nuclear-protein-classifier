import pandas as pd
import numpy as np
import re

wd = '/home/cirofdo/Documents/Multiresolution-nuclear-protein-classifier/'
#wd = 'C:/Users/cirof/Documents/Multiresolution-nuclear-protein-classifier-organize-data/'




###
# Pfam data

# Pfam proteins associated with nucleus terms and membrane terms in keyword search
df_pfam_locations = pd.read_csv(wd + 'input/pfam_nucleus_membrane_data.csv')

# The searched terms
nucleus_terms = ['chromossome', 'chromatin', 'nucleus']
membrane_terms = ['membrane', 'cytoplasm', 'cytoskeleton', 'cytosol']

# Add variable to identify if is a nucleus or membrane term
df_pfam_locations['flag_nucleus'] = np.where(df_pfam_locations['keyword'].isin(nucleus_terms), 1, 0)
df_pfam_locations['flag_membrane'] = np.where(df_pfam_locations['keyword'].isin(membrane_terms), 1, 0)
df_pfam_locations.shape


# The Pfam keyword search find the same accession in different terms
# so I will group these values
df_pfam_locations = df_pfam_locations.groupby('accession')[['flag_nucleus', 'flag_membrane']].max().reset_index()
df_pfam_locations.head(2)
df_pfam_locations.shape




###
# HMM output DataFrame

# HMM output dataframe
df_hmm = pd.read_csv(wd + 'output/df_t_cruzi_hmm.csv', low_memory=False)

# Remove any character after dot ('.')
df_hmm.accession = df_hmm.accession.apply(lambda x: re.sub(r'\..*', '', x.strip()))
df_hmm.target_name = df_hmm.target_name.apply(lambda x: x.strip())
df_hmm.query_name = df_hmm.query_name.apply(lambda x: x.strip())
df_hmm.shape
df_hmm.head(2)


###
# Swissprot data
df_swissprot = pd.read_csv(wd + 'output/df_swiss_prot_t_cruzi.csv')
df_swissprot.drop('Unnamed: 0', axis=1, inplace=True)
df_swissprot.head(2)
df_swissprot.shape

###
# Adjusting variables
df_swissprot['accession'] = df_swissprot.iteration_query_def.str.split('|', expand=True).iloc[:,1]
df_swissprot['query_name'] = df_swissprot.query_id.str.split('|', expand=True).iloc[:,0]













df_hmm[['accession', 'query_name']]





df_pfam_locations.shape

df_pfam_locations.merge(df_hmm[['accession', 'query_name']], how='inner')



















###
# Creates final dataframes with nucleus/membrane hmm scores


# Now I merge these pfam accessions with T cruzi hmm output data
df_hmm = df_hmm.merge(df_pfam_locations, how='left')
df_hmm_pfam = df_hmm[ (df_hmm.flag_nucleus.notna()) & (df_hmm.flag_membrane.notna())].reset_index()
df_hmm_pfam.head(2)
df_hmm_pfam.shape


# Now I merge the swissprot on hmm+pfam data
teste = df_hmm_pfam.merge(df_swissprot, left_on='query_name', right_on='subject_id', how='left')

teste[teste.subject_id.notna()]



df_swissprot.merge(df_hmm[['query_name', 'remove']].drop_duplicates(), left_on='subject_id', right_on='query_name')['remove'].value_counts()




df_swissprot.merge(a, left_on='query_id', right_on='accession').shape
