"""
* Name : ***.py
* Author: Donnie Kramer
* Created : ***
* Course: CIS 152 - Data Structure
* Version: 1.0
* OS: Mac OS
* IDE: PyCharm 2021.3.1
* Copyright : This is my own original work 
* based on specifications issued by our instructor
* Description : The purpose of this program is to ***
*            Input: ***
*            Ouput: ***
* Academic Honesty: I attest that this is my original work.
* I have not used unauthorized source code, either modified or
* unmodified. I have not given other fellow student(s) access
* to my program.
"""


import random


def isDNA(seq) -> bool:
    nucleotides = ['A', 'T', 'C', 'G', "\n"]
    for i in seq:
        if i not in nucleotides:
            return False
    return True

def getRaw(seq) -> str:
    nucleotides = ['A', 'T', 'C', 'G']
    raw = ""
    for i in seq:
        if i in nucleotides:
            raw += i
    return raw

def getRandomNucs(seqSize) -> str:
    """Returns a string of random DNA nucleotides of size seqSize"""

    nucleotides = ['A', 'T', 'C', 'G']
    sequence = ""
    for _ in range(seqSize):
        sequence += (nucleotides[random.randint(0, 3)])
    return sequence

def getComplement(seq) -> str:
    """Return the complementary DNA sequence to the inputted sequence"""

    complementaryNucs = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    compSeq = ""
    for x in seq:
        compSeq += complementaryNucs[x]
    return compSeq

def transcribe(sequence) -> str:
    """Return a string of input DNA sequence in RNA format"""

    rna = sequence.replace('T','U')
    return rna

def translate(rna) -> str:
    codons = {
    "UUU" : "F", "CUU" : "L", "AUU" : "I", "GUU" : "V", "UUC" : "F", 
    "CUC" : "L", "AUC" : "I", "GUC" : "V", "UUA" : "L", "CUA" : "L",
    "AUA" : "I", "GUA" : "V", "UUG" : "L", "CUG" : "L", "AUG" : "M",
    "GUG" : "V", "UCU" : "S", "CCU" : "P", "ACU" : "T", "GCU" : "A",
    "UCC" : "S", "CCC" : "P", "ACC" : "T", "GCC" : "A", "UCA" : "S",
    "CCA" : "P", "ACA" : "T", "GCA" : "A", "UCG" : "S", "CCG" : "P",
    "ACG" : "T", "GCG" : "A", "UAU" : "Y", "CAU" : "H", "AAU" : "N",
    "GAU" : "D", "UAC" : "Y", "CAC" : "H", "AAC" : "N", "GAC" : "D",
    "UAA" : "-", "CAA" : "Q", "AAA" : "K", "GAA" : "E", "UAG" : "-",
    "CAG" : "Q", "AAG" : "K", "GAG" : "E", "UGU" : "C", "CGU" : "R",
    "AGU" : "S", "GGU" : "G", "UGC" : "C", "CGC" : "R", "AGC" : "S",
    "GGC" : "G", "UGA" : "-", "CGA" : "R", "AGA" : "R", "GGA" : "G",
    "UGG" : "W", "CGG" : "R", "AGG" : "R", "GGG" : "G"
    }

    protein = ""

    i = 0
    while i <= len(rna)-3:
        if rna[i+2]:
            protein += codons[rna[i] + rna[i+1] + rna[i+2]]
        i += 3
    
    return protein

class orfNode:
    """Node class for ORFs. Stores start and end position of the orf"""

    def __init__(self, startPos=None, endPos=None) -> None:
        if startPos == None:
            self.startPos = 0
        if endPos == None:
            self.endPos = 0


def getORF(sequence) -> list:
    """returns a list of open reading frames from the inputted sequence.
    ORF is defined by start and end positions only."""

    orfs = []
    currentORF = -1
    gene = False

    startCodon = ('A', 'U', 'G')
    stopCodons = [('U', 'A', 'G'), ('U', 'A', 'A'), ('U', 'G', 'A')]

    # skip last 3 characters in string
    i = 0
    current = 0
    while i <len(sequence)-3:
        if not gene and (sequence[i], sequence[i+1], sequence[i+2]) == startCodon:
            gene = True
            current = i
            orfs.append(orfNode())
            currentORF += 1
            orfs[currentORF].startPos = i
        elif gene and (sequence[i], sequence[i+1], sequence[i+2]) in stopCodons:
            gene = False
            i += 3
            orfs[currentORF].endPos = i
            i = current
        if gene:
            i += 3
        else:
            i += 1

    # come back to last 3 characters in string, append to end of last ORF if gene
    if gene and (sequence[-1], sequence[-2], sequence[-3]) not in stopCodons:
        orfs[-1].endPos = len(sequence)

    # prune redudant ORFs
    endPositions = []
    newORFs = []
    for x in orfs:
        if x.endPos not in endPositions:
            newORFs.append(x)
            endPositions.append(x.endPos)

    return newORFs

def sortORFs(array, size) -> list:
    """sorts a list of orfs from largest to smallest"""

    # source: https://www.geeksforgeeks.org/python-program-for-selection-sort/
    for ind in range(size):
        maxIndex = ind

        for j in range(ind + 1, size):
            # select the minimum element in every iteration
            if abs(array[j].endPos - array[j].startPos) > abs(array[maxIndex].endPos - array[maxIndex].startPos):
                maxIndex = j
        # swapping the elements to sort the array
        (array[ind], array[maxIndex]) = (array[maxIndex], array[ind])

    return array


def longestORF(orfs) -> tuple:
    if orfs == []:
        # raise error
        return orfs
    else:
        x = orfs[0]
        for i in range(len(orfs)-1):
            if orfs[i+1].endPos - orfs[i+1].startPos > x.endPos - x.startPos:
                x = orfs[i+1]
        return (x.startPos, x.endPos)

def master(testSeq) -> str:
    compTestSeq = getComplement(testSeq[::-1])
    
    forRNA = transcribe(testSeq)
    revRNA = transcribe(compTestSeq)

    forORFs = getORF(forRNA)
    revORFs = getORF(revRNA)

    for i in revORFs:
        i.startPos, i.endPos = len(compTestSeq)-i.startPos, len(compTestSeq)-i.endPos
    
    allORFs = forORFs + revORFs
    allORFs = sortORFs(allORFs, len(allORFs))

    result = ""
   
    for i in allORFs:
        if i.endPos > i.startPos:
            result += f"{i.startPos+1} {i.endPos} {i.endPos-i.startPos} +\n"
        else:
            result += f"{i.startPos+1} {i.endPos} {i.startPos-i.endPos} -\n"
    
    return result


if __name__ == "__main__":

    testSeq = "GACACCATCGAATGGCGCAAAACCTTTCGCGGTATGGCATGATAGCGCCCGGAAGAGAGTCAATTCAGGG\
TGGTGAATGTGAAACCAGTAACGTTATACGATGTCGCAGAGTATGCCGGTGTCTCTTATCAGACCGTTTC\
CCGCGTGGTGAACCAGGCCAGCCACGTTTCTGCGAAAACGCGGGAAAAAGTGGAAGCGGCGATGGCGGAG\
CTGAATTACATTCCCAACCGCGTGGCACAACAACTGGCGGGCAAACAGTCGTTGCTGATTGGCGTTGCCA\
CCTCCAGTCTGGCCCTGCACGCGCCGTCGCAAATTGTCGCGGCGATTAAATCTCGCGCCGATCAACTGGG\
TGCCAGCGTGGTGGTGTCGATGGTAGAACGAAGCGGCGTCGAAGCCTGTAAAGCGGCGGTGCACAATCTT\
CTCGCGCAACGCGTCAGTGGGCTGATCATTAACTATCCGCTGGATGACCAGGATGCCATTGCTGTGGAAG\
CTGCCTGCACTAATGTTCCGGCGTTATTTCTTGATGTCTCTGACCAGACACCCATCAACAGTATTATTTT\
CTCCCATGAAGACGGTACGCGACTGGGCGTGGAGCATCTGGTCGCATTGGGTCACCAGCAAATCGCGCTG\
TTAGCGGGCCCATTAAGTTCTGTCTCGGCGCGTCTGCGTCTGGCTGGCTGGCATAAATATCTCACTCGCA\
ATCAAATTCAGCCGATAGCGGAACGGGAAGGCGACTGGAGTGCCATGTCCGGTTTTCAACAAACCATGCA\
AATGCTGAATGAGGGCATCGTTCCCACTGCGATGCTGGTTGCCAACGATCAGATGGCGCTGGGCGCAATG\
CGCGCCATTACCGAGTCCGGGCTGCGCGTTGGTGCGGATATCTCGGTAGTGGGATACGACGATACCGAAG\
ACAGCTCATGTTATATCCCGCCGTCAACCACCATCAAACAGGATTTTCGCCTGCTGGGGCAAACCAGCGT\
GGACCGCTTGCTGCAACTCTCTCAGGGCCAGGCGGTGAAGGGCAATCAGCTGTTGCCCGTCTCACTGGTG\
AAAAGAAAAACCACCCTGGCGCCCAATACGCAAACCGCCTCTCCCCGCGCGTTGGCCGATTCATTAATGC\
AGCTGGCACGACAGGTTTCCCGACTGGAAAGCGGGCAGTGAGCGCAACGCAATTAATGTGAGTTAGCTCA\
CTCATTAGGCACCCCAGGCTTTACACTTTATGCTTCCGGCTCGTATGTTGTGTGGAATTGTGAGCGGATA\
ACAATTTCACACAGGAAACAGCTATGACCATGATTACGGATTCACTGGCCGTCGTTTTACAACGTCGTGA\
CTGGGAAAACCCTGGCGTTACCCAACTTAATCGCCTTGCAGCACATCCCCCTTTCGCCAGCTGGCGTAAT\
AGCGAAGAGGCCCGCACCGATCGCCCTTCCCAACAGTTGCGCAGCCTGAATGGCGAATGGCGCTTTGCCT\
GGTTTCCGGCACCAGAAGCGGTGCCGGAAAGCTGGCTGGAGTGCGATCTTCCTGAGGCCGATACTGTCGT\
CGTCCCCTCAAACTGGCAGATGCACGGTTACGATGCGCCCATCTACACCAACGTAACCTATCCCATTACG\
GTCAATCCGCCGTTTGTTCCCACGGAGAATCCGACGGGTTGTTACTCGCTCACATTTAATGTTGATGAAA\
GCTGGCTACAGGAAGGCCAGACGCGAATTATTTTTGATGGCGTTAACTCGGCGTTTCATCTGTGGTGCAA\
CGGGCGCTGGGTCGGTTACGGCCAGGACAGTCGTTTGCCGTCTGAATTTGACCTGAGCGCATTTTTACGC\
GCCGGAGAAAACCGCCTCGCGGTGATGGTGCTGCGTTGGAGTGACGGCAGTTATCTGGAAGATCAGGATA\
TGTGGCGGATGAGCGGCATTTTCCGTGACGTCTCGTTGCTGCATAAACCGACTACACAAATCAGCGATTT\
CCATGTTGCCACTCGCTTTAATGATGATTTCAGCCGCGCTGTACTGGAGGCTGAAGTTCAGATGTGCGGC\
GAGTTGCGTGACTACCTACGGGTAACAGTTTCTTTATGGCAGGGTGAAACGCAGGTCGCCAGCGGCACCG\
CGCCTTTCGGCGGTGAAATTATCGATGAGCGTGGTGGTTATGCCGATCGCGTCACACTACGTCTGAACGT\
CGAAAACCCGAAACTGTGGAGCGCCGAAATCCCGAATCTCTATCGTGCGGTGGTTGAACTGCACACCGCC\
GACGGCACGCTGATTGAAGCAGAAGCCTGCGATGTCGGTTTCCGCGAGGTGCGGATTGAAAATGGTCTGC\
TGCTGCTGAACGGCAAGCCGTTGCTGATTCGAGGCGTTAACCGTCACGAGCATCATCCTCTGCATGGTCA\
GGTCATGGATGAGCAGACGATGGTGCAGGATATCCTGCTGATGAAGCAGAACAACTTTAACGCCGTGCGC\
TGTTCGCATTATCCGAACCATCCGCTGTGGTACACGCTGTGCGACCGCTACGGCCTGTATGTGGTGGATG\
AAGCCAATATTGAAACCCACGGCATGGTGCCAATGAATCGTCTGACCGATGATCCGCGCTGGCTACCGGC\
GATGAGCGAACGCGTAACGCGAATGGTGCAGCGCGATCGTAATCACCCGAGTGTGATCATCTGGTCGCTG\
GGGAATGAATCAGGCCACGGCGCTAATCACGACGCGCTGTATCGCTGGATCAAATCTGTCGATCCTTCCC\
GCCCGGTGCAGTATGAAGGCGGCGGAGCCGACACCACGGCCACCGATATTATTTGCCCGATGTACGCGCG\
CGTGGATGAAGACCAGCCCTTCCCGGCTGTGCCGAAATGGTCCATCAAAAAATGGCTTTCGCTACCTGGA\
GAGACGCGCCCGCTGATCCTTTGCGAATACGCCCACGCGATGGGTAACAGTCTTGGCGGTTTCGCTAAAT\
ACTGGCAGGCGTTTCGTCAGTATCCCCGTTTACAGGGCGGCTTCGTCTGGGACTGGGTGGATCAGTCGCT\
GATTAAATATGATGAAAACGGCAACCCGTGGTCGGCTTACGGCGGTGATTTTGGCGATACGCCGAACGAT\
CGCCAGTTCTGTATGAACGGTCTGGTCTTTGCCGACCGCACGCCGCATCCAGCGCTGACGGAAGCAAAAC\
ACCAGCAGCAGTTTTTCCAGTTCCGTTTATCCGGGCAAACCATCGAAGTGACCAGCGAATACCTGTTCCG\
TCATAGCGATAACGAGCTCCTGCACTGGATGGTGGCGCTGGATGGTAAGCCGCTGGCAAGCGGTGAAGTG\
CCTCTGGATGTCGCTCCACAAGGTAAACAGTTGATTGAACTGCCTGAACTACCGCAGCCGGAGAGCGCCG\
GGCAACTCTGGCTCACAGTACGCGTAGTGCAACCGAACGCGACCGCATGGTCAGAAGCCGGGCACATCAG\
CGCCTGGCAGCAGTGGCGTCTGGCGGAAAACCTCAGTGTGACGCTCCCCGCCGCGTCCCACGCCATCCCG\
CATCTGACCACCAGCGAAATGGATTTTTGCATCGAGCTGGGTAATAAGCGTTGGCAATTTAACCGCCAGT\
CAGGCTTTCTTTCACAGATGTGGATTGGCGATAAAAAACAACTGCTGACGCCGCTGCGCGATCAGTTCAC\
CCGTGCACCGCTGGATAACGACATTGGCGTAAGTGAAGCGACCCGCATTGACCCTAACGCCTGGGTCGAA\
CGCTGGAAGGCGGCGGGCCATTACCAGGCCGAAGCAGCGTTGTTGCAGTGCACGGCAGATACACTTGCTG\
ATGCGGTGCTGATTACGACCGCTCACGCGTGGCAGCATCAGGGGAAAACCTTATTTATCAGCCGGAAAAC\
CTACCGGATTGATGGTAGTGGTCAAATGGCGATTACCGTTGATGTTGAAGTGGCGAGCGATACACCGCAT\
CCGGCGCGGATTGGCCTGAACTGCCAGCTGGCGCAGGTAGCAGAGCGGGTAAACTGGCTCGGATTAGGGC\
CGCAAGAAAACTATCCCGACCGCCTTACTGCCGCCTGTTTTGACCGCTGGGATCTGCCATTGTCAGACAT\
GTATACCCCGTACGTCTTCCCGAGCGAAAACGGTCTGCGCTGCGGGACGCGCGAATTGAATTATGGCCCA\
CACCAGTGGCGCGGCGACTTCCAGTTCAACATCAGCCGCTACAGTCAACAGCAACTGATGGAAACCAGCC\
ATCGCCATCTGCTGCACGCGGAAGAAGGCACATGGCTGAATATCGACGGTTTCCATATGGGGATTGGTGG\
CGACGACTCCTGGAGCCCGTCAGTATCGGCGGAATTCCAGCTGAGCGCCGGTCGCTACCATTACCAGTTG\
GTCTGGTGTCAAAAATAATAATAACCGGGCAGGCCATGTCTGCCCGTATTTCGCGTAAGGAAATCCATTA\
TGTACTATTTAAAAAACACAAACTTTTGGATGTTCGGTTTATTCTTTTTCTTTTACTTTTTTATCATGGG\
AGCCTACTTCCCGTTTTTCCCGATTTGGCTACATGACATCAACCATATCAGCAAAAGTGATACGGGTATT\
ATTTTTGCCGCTATTTCTCTGTTCTCGCTATTATTCCAACCGCTGTTTGGTCTGCTTTCTGACAAACTCG\
GGCTGCGCAAATACCTGCTGTGGATTATTACCGGCATGTTAGTGATGTTTGCGCCGTTCTTTATTTTTAT\
CTTCGGGCCACTGTTACAATACAACATTTTAGTAGGATCGATTGTTGGTGGTATTTATCTAGGCTTTTGT\
TTTAACGCCGGTGCGCCAGCAGTAGAGGCATTTATTGAGAAAGTCAGCCGTCGCAGTAATTTCGAATTTG\
GTCGCGCGCGGATGTTTGGCTGTGTTGGCTGGGCGCTGTGTGCCTCGATTGTCGGCATCATGTTCACCAT\
CAATAATCAGTTTGTTTTCTGGCTGGGCTCTGGCTGTGCACTCATCCTCGCCGTTTTACTCTTTTTCGCC\
AAAACGGATGCGCCCTCTTCTGCCACGGTTGCCAATGCGGTAGGTGCCAACCATTCGGCATTTAGCCTTA\
AGCTGGCACTGGAACTGTTCAGACAGCCAAAACTGTGGTTTTTGTCACTGTATGTTATTGGCGTTTCCTG\
CACCTACGATGTTTTTGACCAACAGTTTGCTAATTTCTTTACTTCGTTCTTTGCTACCGGTGAACAGGGT\
ACGCGGGTATTTGGCTACGTAACGACAATGGGCGAATTACTTAACGCCTCGATTATGTTCTTTGCGCCAC\
TGATCATTAATCGCATCGGTGGGAAAAACGCCCTGCTGCTGGCTGGCACTATTATGTCTGTACGTATTAT\
TGGCTCATCGTTCGCCACCTCAGCGCTGGAAGTGGTTATTCTGAAAACGCTGCATATGTTTGAAGTACCG\
TTCCTGCTGGTGGGCTGCTTTAAATATATTACCAGCCAGTTTGAAGTGCGTTTTTCAGCGACGATTTATC\
TGGTCTGTTTCTGCTTCTTTAAGCAACTGGCGATGATTTTTATGTCTGTACTGGCGGGCAATATGTATGA\
AAGCATCGGTTTCCAGGGCGCTTATCTGGTGCTGGGTCTGGTGGCGCTGGGCTTCACCTTAATTTCCGTG\
TTCACGCTTAGCGGCCCCGGCCCGCTTTCCCTGCTGCGTCGTCAGGTGAATGAAGTCGCTTAAGCAATCA\
ATGTCGGATGCGGCGCGACGCTTATCCGACCAACATATCATAACGGAGTGATCGCATTGAACATGCCAAT\
GACCGAAAGAATAAGAGCAGGCAAGCTATTTACCGATATGTGCGAAGGCTTACCGGAAAAAAGACTTCGT\
GGGAAAACGTTAATGTATGAGTTTAATCACTCGCATCCATCAGAAGTTGAAAAAAGAGAAAGCCTGATTA\
AAGAAATGTTTGCCACGGTAGGGGAAAACGCCTGGGTAGAACCGCCTGTCTATTTCTCTTACGGTTCCAA\
CATCCATATAGGCCGCAATTTTTATGCAAATTTCAATTTAACCATTGTCGATGACTACACGGTAACAATC\
GGTGATAACGTACTGATTGCACCCAACGTTACTCTTTCCGTTACGGGACACCCTGTACACCATGAATTGA\
GAAAAAACGGCGAGATGTACTCTTTTCCGATAACGATTGGCAATAACGTCTGGATCGGAAGTCATGTGGT\
TATTAATCCAGGCGTCACCATCGGGGATAATTCTGTTATTGGCGCGGGTAGTATCGTCACAAAAGACATT\
CCACCAAACGTCGTGGCGGCTGGCGTTCCTTGTCGGGTTATTCGCGAAATAAACGACCGGGATAAGCACT\
ATTATTTCAAAGATTATAAAGTTGAATCGTCAGTTTAAATTATAAAAATTGCCTGATACGCTGCGCTTAT\
CAGGCCTACAAGTTCAGCGATCTACATTAGCCGCATCCGGCATGAACAAAGCGCAGGAACAAGCGTCGCA\
TCATGCCTCTTTGACCCACAGCTGCGGAAAACGTACTGGTGCAAAACGCAGGGTTATGATCATCAGCCCA\
ACGACGCACAGCGCATGAAATGCCCAGTCCATCAGGTAATTGCCGCTGATACTACGCAGCACGCCAGAAA\
ACCACGGGGCAAGCCCGGCGATGATAAAACCGATTCCCTGCATAAACGCCACCAGCTTGCCAGCAATAGC\
CGGTTGCACAGAGTGATCGAGCGCCAGCAGCAAACAGAGCGGAAACGCGCCGCCCAGACCTAACCCACAC\
ACCATCGCCCACAATACCGGCAATTGCATCGGCAGCCAGATAAAGCCGCAGAACCCCACCAGTTGTAACA\
CCAGCGCCAGCATTAACAGTTTGCGCCGATCCTGATGGCGAGCCATAGCAGGCATCAGCAAAGCTCCTGC\
GGCTTGCCCAAGCGTCATCAATGCCAGTAAGGAACCGCTGTACTGCGCGCTGGCACCAATCTCAATATAG\
AAAGCGGGTAACCAGGCAATCAGGCTGGCGTAACCGCCGTTAATCAGACCGAAGTAAACACCCAGCGTCC\
ACGCGCGGGGAGTGAATACCACGCGAACCGGAGTGGTTGTTGTCTTGTGGGAAGAGGCGACCTCGCGGGC\
GCTTTGCCACCACCAGGCAAAGAGCGCAACAACGGCAGGCAGCGCCACCAGGCGAGTGTTTGATACCAGG\
TTTCGCTATGTTGAACTAACCAGGGCGTTATGGCGGCACCAAGCCCACCGCCGCCCATCAGAGCCGCGGA\
CCACAGCCCCATCACCAGTGGCGTGCGCTGCTGAAACCGCCGTTTAATCACCGAAGCATCACCGCCTGAA\
TGATGCCGATCCCCACCCCACCAAGCAGTGCGCTGCTAAGCAGCAGCGCACTTTGCGGGTAAAGCTCACG\
CATCAATGCACCGACGGCAATCAGCAACAGACTGATGGCGACACTGCGACGTTCGCTGACATGCTGATGA\
AGCCAGCTTCCGGCCAGCGCCAGCCCGCCCATGGTAACCACCGGCAGAGCGGTCGAC"

    compTestSeq = getComplement(testSeq[::-1])
    
    forRNA = transcribe(testSeq)
    revRNA = transcribe(compTestSeq)

    forORFs = getORF(forRNA)
    revORFs = getORF(revRNA)

    for i in revORFs:
        i.startPos, i.endPos = len(compTestSeq)-i.startPos, len(compTestSeq)-i.endPos
    
    allORFs = forORFs + revORFs
    allORFs = sortORFs(allORFs, len(allORFs))
   
    for i in allORFs:
        if i.endPos > i.startPos:
            print(i.startPos+1, i.endPos, i.endPos-i.startPos, "+")
        else:
            print(i.startPos+1, i.endPos, i.startPos-i.endPos, "-")

