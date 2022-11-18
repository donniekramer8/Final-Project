from Bio import Entrez

Entrez.email = "donniekramer@gmail.com"
handle = Entrez.efetch(db="nucleotide", id="AY851612", rettype="gb", retmode="text")
print(handle.readline().strip())
