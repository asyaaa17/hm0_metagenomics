from Bio import SeqIO
import random

def read_fasta(file_path):
    sequences = SeqIO.to_dict(SeqIO.parse(file_path, "fasta"))
    return sequences

file_path = 'GCF_000027325.1_ASM2732v1_genomic.fna'

sequences = read_fasta(file_path)
print(sequences)


###Prediction
def find_orfs(sequence):
    orfs = []
    start_codon = "ATG"
    stop_codons = ["TAA", "TAG", "TGA"]

    for i in range(len(sequence)-2):
        if sequence[i:i+3] == start_codon:
            for j in range(i+3, len(sequence), 3):
                if sequence[j:j+3] in stop_codons:
                    orfs.append((i, j+3))
                    break

    return orfs

def predict_genes(sequences):
    predicted_genes = {}

    for header, sequence in sequences.items():
        orfs = find_orfs(str(sequence.seq))
        predicted_genes[header] = orfs

    return predicted_genes

def write_bed_file(predicted_genes, output_file):
    with open(output_file, 'w') as f:
        for header, orfs in predicted_genes.items():
            for i, j in orfs:
                f.write(f'{header}\t{i}\t{j}\n')


predicted_genes = predict_genes(sequences)
write_bed_file(predicted_genes, 'predicted_genes.bed')




