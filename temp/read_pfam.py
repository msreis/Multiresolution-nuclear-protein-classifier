import pandas as pd
from Bio import SeqIO
#records = list(SeqIO.parse("Pfam-A.fasta", "fasta"))
records = list(SeqIO.parse("T_cruzi_TriTryp-25.fasta", "fasta"))

for i in range(10):
	print(records[i])