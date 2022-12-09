"""
* Name : functions.py
* Author: Donnie Kramer
* Created : 11/12/22
* Course: CIS 152 - Data Structure
* Version: 1.0
* OS: Mac OS
* IDE: PyCharm 2021.3.1
* Copyright : This is my own original work
* based on specifications issued by our instructor
* Description : This main function in this file finds open reading frames
within a DNA strand. An open reading frame is a string of DNA letters between a
start and a stop codon. A start codon is always AUG, but a stop codon can be
one of 3 different 3-letter strings. The reason why you might want to find an
open reading frame (ORF for short) is that long ORFs are typically genes. A
gene will be transcribed into RNA, and that will then get translated into a
protein.
*            Input: A DNA sequence
*            Output: A list of Open Reading Frames, sorted in decreasing
order of length. Start and End positions on input DNA strand are given, as well
as if its on the forward or reverse strand, and also the protein sequence.
* Academic Honesty: I attest that this is my original work.
* I have not used unauthorized source code, either modified or
* unmodified. I have not given other fellow student(s) access
* to my program.
"""


import random


def isDNA(seq) -> bool:  # GOOD
    """Returns true if inputted sequence is DNA"""

    nucleotides = ['A', 'T', 'C', 'G', "\n"]
    return all(i in nucleotides for i in seq)


def getRaw(seq) -> str:  # GOOD
    """Returns a string of only the raw nucleotides"""

    nucleotides = ['A', 'T', 'C', 'G']
    return "".join(i for i in seq if i in nucleotides)


# the function below is not used here, but I like it for my own playing around
# so I will not delete it, but for the purposes of this assignment, do not worry
# about it

# def getRandomNucs(seqSize) -> str:  # GOOD
#     """Returns a string of random DNA nucleotides of size seqSize"""

#     nucleotides = ['A', 'T', 'C', 'G']
#     return "".join(nucleotides[random.randint(0, 3)] for _ in range(seqSize))


def getComplement(DNA) -> str:  # GOOD
    """Return the complementary DNA sequence to the inputted sequence"""

    complementaryNucs = {'A': 'T', 'U': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    return "".join(complementaryNucs[x] for x in DNA)


def transcribe(DNA) -> str:  # GOOD
    """Return a string of input DNA sequence in RNA format"""

    return DNA.replace('T', 'U')


def translate(RNA) -> str:  # GOOD
    """Translates RNA -> Protein sequence"""

    codons = {
        "UUU": "F", "CUU": "L", "AUU": "I", "GUU": "V", "UUC": "F",
        "CUC": "L", "AUC": "I", "GUC": "V", "UUA": "L", "CUA": "L",
        "AUA": "I", "GUA": "V", "UUG": "L", "CUG": "L", "AUG": "M",
        "GUG": "V", "UCU": "S", "CCU": "P", "ACU": "T", "GCU": "A",
        "UCC": "S", "CCC": "P", "ACC": "T", "GCC": "A", "UCA": "S",
        "CCA": "P", "ACA": "T", "GCA": "A", "UCG": "S", "CCG": "P",
        "ACG": "T", "GCG": "A", "UAU": "Y", "CAU": "H", "AAU": "N",
        "GAU": "D", "UAC": "Y", "CAC": "H", "AAC": "N", "GAC": "D",
        "UAA": "-", "CAA": "Q", "AAA": "K", "GAA": "E", "UAG": "-",
        "CAG": "Q", "AAG": "K", "GAG": "E", "UGU": "C", "CGU": "R",
        "AGU": "S", "GGU": "G", "UGC": "C", "CGC": "R", "AGC": "S",
        "GGC": "G", "UGA": "-", "CGA": "R", "AGA": "R", "GGA": "G",
        "UGG": "W", "CGG": "R", "AGG": "R", "GGG": "G"
    }

    protein = ""

    i = 0
    while i <= len(RNA)-3:
        if RNA[i+2]:
            protein += codons[RNA[i] + RNA[i+1] + RNA[i+2]]
        i += 3

    return protein


class orf:
    """Class for ORFs. Stores start and end position of the orf"""
    # this class initially made more sense because I had other attributes such
    # as the protein sequence, length, etc. I ended up removing those and only
    # including the start and end positions. I did this because I felt like it
    # was a waste of time to calculate those things for each orf. The purpose of
    # this program after all is to find the longest orf, and that is all. So, I
    # ended up just calling functions to find the protein sequence and etc.
    # later on only in the longest orf.

    def __init__(self) -> None:
        self.startPos = 0
        self.endPos = 0


def getORFs(RNA) -> list:
    """returns a list of open reading frames from the inputted sequence.
    ORF is defined by start and end positions only."""

    orfs = []
    currentORF = -1
    gene = False

    startCodon = ('A', 'U', 'G')
    stopCodons = [('U', 'A', 'G'), ('U', 'A', 'A'), ('U', 'G', 'A')]

    i = 0
    current = 0
    while i < len(RNA)-3:  # skip last 3 characters in string
        if not gene and (RNA[i], RNA[i+1], RNA[i+2]) == startCodon:
            gene = True
            current = i
            orfs.append(orf())
            currentORF += 1
            orfs[currentORF].startPos = i
        elif gene and (RNA[i], RNA[i+1], RNA[i+2]) in stopCodons:
            gene = False
            i += 3
            orfs[currentORF].endPos = i
            i = current
        i += 3 if gene else 1

    # come back to last 3 characters in string, append to end of the last ORF
    # if gene
    if gene and (RNA[-1], RNA[-2], RNA[-3]) not in stopCodons:
        orfs[-1].endPos = len(RNA)  # ORF ends at the end of the sequence

    # remove redundant ORFs (one open reading frame within another)
    endPositions = []
    newORFs = []
    for x in orfs:
        if x.endPos not in endPositions:
            newORFs.append(x)
            endPositions.append(x.endPos)
    # note: iterating through 'orfs' list, its already sorted, so the next
    # 'x.startPos' is always going to be larger than the previous

    return newORFs


def sortORFs(orfArr, size) -> list:
    """sorts a list of orfs from largest to smallest"""

    # selection sort

    for ind in range(size):
        maxIndex = ind

        for j in range(ind + 1, size):
            # select the maximum length orf in every iteration
            if abs(orfArr[j].endPos - orfArr[j].startPos) > \
                    abs(orfArr[maxIndex].endPos - orfArr[maxIndex].startPos):
                maxIndex = j
        # swap the orfs
        (orfArr[ind], orfArr[maxIndex]) = (orfArr[maxIndex], orfArr[ind])

    return orfArr


def longestORF(DNA) -> str:
    """Returns protein sequence string of longest ORF in of the inputted DNA
    strand"""

    orfs = getAllOrfs(DNA)

    if orfs == []:
        return ''
    x = orfs[0]
    for i in range(len(orfs)-1):
        if orfs[i+1].endPos - orfs[i+1].startPos > x.endPos - x.startPos:
            x = orfs[i+1]

    RNA = transcribe(DNA) if x.endPos > x.startPos else compRNA(DNA)

    return getProtein(RNA, x.startPos, x.endPos)


def compRNA(DNA) -> str:
    """Return a string of the RNA strand complementary to the inputted DNA
    sequence in the 5' -> 3' direction"""

    return transcribe(getComplement(DNA[::-1]))


def getProtein(RNAseq, start, end) -> str:
    """Returns sequence string after its location start and end positinos are
    inputted"""

    # An example of one of the functions I made instead of doing more with the
    # orf class

    if end > start:
        return str(translate(RNAseq[start:end]))
    else:
        return str(translate(RNAseq[end:start][::-1]))


def getAllOrfs(DNA) -> list:
    """Returns list of all non-redundant ORFs of a DNA string and it's
    complementary sequence. List is made up of orfNode class objects. This is
    different from getORFs because it gets orfs for both the forward and
    reverse strands."""

    forRNA = transcribe(DNA)
    revRNA = compRNA(DNA)

    forORFs = getORFs(forRNA)
    revORFs = getORFs(revRNA)

    for i in revORFs:  # switch start/end positions to reflect direction of RNA
        i.startPos, i.endPos = len(revRNA) - \
            i.startPos, len(revRNA)-i.endPos

    allORFs = forORFs + revORFs
    allORFs = sortORFs(allORFs, len(allORFs))

    return allORFs


def main(DNA) -> str:
    """Input a sequence and get a list of ORfs in return"""

    # defining these here to print below
    forRNA = transcribe(DNA)
    revRNA = compRNA(DNA)[::-1]

    allORFs = getAllOrfs(DNA)

    result = ""
    for i in allORFs:
        if i.endPos > i.startPos:
            result += f"Start: {i.startPos+1}\nEnd: {i.endPos}\nLength: {i.endPos-i.startPos}\n+\n"
            result += f"{translate(forRNA[i.startPos:i.endPos])}\n\n"
        else:
            result += f"Start: {i.startPos+1}\nEnd: {i.endPos}\nLength: {i.startPos-i.endPos}\n-\n"
            result += f"{translate(revRNA[i.endPos:i.startPos][::-1])}\n\n"
            # I know I have reversed the revRNA list like 3 times now, but it
            # hurts my brain when I think about it and this works

    return result


if __name__ == "__main__":

    testSeq = "\
GACACCATCGAATGGCGCAAAACCTTTCGCGGTATGGCATGATAGCGCCCGGAAGAGAGTCAATTCAGGG\
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

    print(main(testSeq))
    print(longestORF(testSeq))
