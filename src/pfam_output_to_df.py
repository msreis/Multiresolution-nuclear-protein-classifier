import pandas as pd

wd = '/home/cirofdo/Documents/Multiresolution-nuclear-protein-classifier/'

col_names = ['target_name','accession','query_name','remove','e_value','score',
            'bias','e_value2','score_2','bias_2','exp','reg','clu','ov','env','dom',
            'rep','inc','description_of_target']


df = pd.DataFrame(columns=col_names)
lines = [line.rstrip('\n') for line in open(wd + 'output/output-file-tbl')]


for i in range(len(lines)-13):
    df.loc[i] = [lines[i+3][:21],lines[i+3][21:32],lines[i+3][32:51],lines[i+3][51:65],
                 lines[i+3][65:75],lines[i+3][75:80],lines[i+3][82:89],lines[i+3][89:98],
                 lines[i+3][98:105],lines[i+3][105:112],lines[i+3][112:118],lines[i+3][118:122],
                 lines[i+3][122:126],lines[i+3][126:130],lines[i+3][130:134],lines[i+3][134:138],
                 lines[i+3][138:142],lines[i+3][142:144],lines[i+3][-(len(lines[i+3])-144):]]

df.to_csv(wd + 'output/df_t_cruzi_hmm.csv', index=False)
