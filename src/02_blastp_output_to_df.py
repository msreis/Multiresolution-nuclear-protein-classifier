import pandas as pd

wd = '/home/cirofdo/Documents/Multiresolution-nuclear-protein-classifier/'

col_names = ['query_id','subject_id','pct_identity','aln_length','n_of_mismatches','gap_openings',
			 'q_start','q_end','s_start','s_end','e_value','bit_score']

df = pd.read_csv(wd + 'output/swiss-prot--T-cruzi.blastp', sep='	', names=col_names)
df.query_id = df.query_id.apply(lambda x: x.replace('sp|', '')[:6])

df.to_csv(wd + 'output/df_swiss_prot_t_cruzi.csv', index=False)
