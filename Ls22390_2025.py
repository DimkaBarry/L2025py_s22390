# CEL PROGRAMU:
# Program generuje losową sekwencję DNA w formacie FASTA, zapisuje ją do pliku oraz wyświetla statystyki.
# KONTEKST ZASTOSOWANIA:
# Ćwiczenie laboratoryjne z bioinformatyki – wykorzystanie LLM do tworzenia kodu oraz jego modyfikacji.

import random

# Funkcja generująca losową sekwencję DNA
def generate_dna_sequence(length):
    return ''.join(random.choices('ACGT', k=length))

# Funkcja wstawiająca imię w losowym miejscu sekwencji
def insert_name(sequence, name):
    pos = random.randint(0, len(sequence))
    return sequence[:pos] + name + sequence[pos:]

# Funkcja licząca statystyki sekwencji
def calculate_stats(sequence):
    counts = {nuc: sequence.count(nuc) for nuc in 'ACGT'}
    total = sum(counts.values())
    stats = {nuc: round((count / total) * 100, 1) for nuc, count in counts.items()}
    cg = counts['C'] + counts['G']
    at = counts['A'] + counts['T']
    ratio_cg_at = round((cg / total) * 100, 1)
    return stats, ratio_cg_at

# Pobranie danych od użytkownika
# ULPSZENIE 1: Walidacja długości sekwencji
# ORIGINAL:
# length = int(input("Podaj długość sekwencji: "))
# MODIFIED (sprawdza, czy długość jest dodatnią liczbą całkowitą)
while True:
    try:
        length = int(input("Podaj długość sekwencji: "))
        if length > 0:
            break
        else:
            print("Długość musi być większa niż 0.")
    except ValueError:
        print("Wprowadź poprawną liczbę całkowitą.")

id_seq = input("Podaj ID sekwencji: ")
description = input("Podaj opis sekwencji: ")
name = input("Podaj imię: ")

# Generowanie i modyfikacja sekwencji
original_sequence = generate_dna_sequence(length)
sequence_with_name = insert_name(original_sequence, name)

# Obliczenie statystyk (bez imienia)
stats, ratio_cg_at = calculate_stats(original_sequence)

# Zapis do pliku FASTA
# ULPSZENIE 2: Podział sekwencji w pliku FASTA na linie po 60 znaków
# ORIGINAL:
# fasta_file.write(sequence_with_name + '\\n')
# MODIFIED (dla lepszej czytelności zgodnie z konwencją FASTA)
filename = f"{id_seq}.fasta"
with open(filename, 'w') as fasta_file:
    fasta_file.write(f">{id_seq} {description}\n")
    for i in range(0, len(sequence_with_name), 60):
        fasta_file.write(sequence_with_name[i:i+60] + '\n')

# Wyświetlenie statystyk
print(f"Sekwencja została zapisana do pliku {filename}\n")
print("Statystyki sekwencji:")
for nuc, percent in stats.items():
    print(f"{nuc}: {percent}%")
print(f"%CG: {ratio_cg_at}%")

# ULPSZENIE 3: Zapis statystyk do osobnego pliku .txt
# (pomaga w archiwizacji wyników i analizie offline)
stats_filename = f"{id_seq}_stats.txt"
with open(stats_filename, 'w') as stats_file:
    stats_file.write(f"Statystyki sekwencji: {id_seq}\n")
    for nuc, percent in stats.items():
        stats_file.write(f"{nuc}: {percent}%\n")
    stats_file.write(f"%CG: {ratio_cg_at}%\n")