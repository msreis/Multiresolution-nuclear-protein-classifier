library(XML)

#wd <- '/home/cirofdo/Documents/Multiresolution-nuclear-protein-classifier/'
wd <- 'C:/Users/cirof/Documents/Multiresolution-nuclear-protein-classifier-organize-data/'

setwd(wd)

data <- xmlParse('output/swiss-prot--T-cruzi.blastp.xml')
xml_data <- xmlToList(data)


iterations <- as.list(xml_data$BlastOutput_iterations)

df_swiss_prot_t_cruzi <- data.frame()

for(i in 1:length(iterations)){
  df_swiss_prot_t_cruzi[i, 'iteration_query_def'] <- iterations[i]$Iteration$`Iteration_query-def`
  df_swiss_prot_t_cruzi[i, 'aln_length'] <- as.integer(iterations[i]$Iteration$`Iteration_query-len`)
  df_swiss_prot_t_cruzi[i, 'flag_hit'] <- ifelse(iterations[i]$Iteration$Iteration_hits=="\n", 0, length(iterations[i]$Iteration$Iteration_hits$Hit$Hit_hsps))
  if(df_swiss_prot_t_cruzi[i, 'flag_hit']>=1) {
    df_swiss_prot_t_cruzi[i, 'query_id'] <- iterations[i]$Iteration$Iteration_hits$`Hit`$Hit_def
    #df_swiss_prot_t_cruzi[i, 'e_value'] <- iterations[i]$Iteration$Iteration_hits$`Hit`$Hit_hsps$`Hsp`$Hsp_evalue
    #df_swiss_prot_t_cruzi[i, 'bit_score'] <- iterations[i]$Iteration$Iteration_hits$`Hit`$Hit_hsps$`Hsp`$`Hsp_bit-score`
  }
}



iterations[1]$Iteration$Iteration_hits$`Hit`$Hit_num

iterations[11]$Iteration$Iteration_hits$`Hit`$Hit_def


