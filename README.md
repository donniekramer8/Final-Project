# Final-Project

This is a bacterial longest-open-reading-frame-finder program for my final project in Data Structures.

I made this program because I am currently enrolled in a masters program for bioinformatics. I thought it would be cool to apply some of the stuff I learned in this class to area of interest.

This is built for bacterial DNA only. This program only takes into consideration start and stop codons. Splice sites, promoters, etc. are not taken into consideration. This is not a gene finder, it is a longest open reading frame finder.

Running the gui.py file will bring up a user interface. Enter in your DNA sequence there. Not sure what to enter? Here are a few links you could use.

https://www.ncbi.nlm.nih.gov/nuccore/J01636.1
https://www.ncbi.nlm.nih.gov/nuccore/NZ_JAEMHT010000072.1
https://www.ncbi.nlm.nih.gov/nuccore/NZ_JAEMHT010000062.1
https://www.ncbi.nlm.nih.gov/nuccore/NZ_JAEMHT010000058.1

When you click the link, click 'FASTA' in upper left corner. Then, copy paste the DNA sequence. Note: Do not include the line starting with '>', I did not have the time to make this program ignore that line.

If you want to try others, go to that ncbi page and search 'shotgun bacteria' and follow those same instruction. This shows you big sequences of bacterial DNA that might have some genes in them.

Then, you could try searching the longest open reading frame's protein sequence to see if it matches up with a protein in their database.

To do that, copy the protein sequence "without the '-' at the end" and paste it into the box at this page:
https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastp&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome

It might take a minute, but it will show you if your ORF is indeed a protein-coding gene!
