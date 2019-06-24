import pandas as pd

wd = '/home/cirofdo/Documents/Multiresolution-nuclear-protein-classifier/'

f = open(wd + 'output/blastn_header.txt', 'r')
col_names = f.read().split()

df = pd.read_csv(wd + 'output/swiss-prot--T-cruzi.blastp', sep='	', names=col_names)
df.query_id = df.query_id.apply(lambda x: x.replace('sp|', '')[:6])

df.to_csv(wd + 'output/df_swiss_prot_t_cruzi.csv', index=False)
