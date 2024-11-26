# файл: calculate_molecular_mass.py

from functools import reduce
import re

# Атомные массы элементов
atomic_masses = {
    'H': 1.008,
    'O': 15.999,
    'S': 32.066,
    'Na': 22.990,
    'Cl': 35.453,
    'K': 39.098
}

# Входные данные
molecules = ['H2-S-O4', 'H2-O', 'NA-CL', 'H-CL', 'K-CL']

def normalize_molecule(molecule: str):
    """
    Приводит обозначения атомов в молекуле к правильному регистру.
    Например: 'NA-CL' -> 'Na-Cl'
    """
    molecule = molecule.upper()
    components = re.findall(r'[A-Z][A-Z]?', molecule)
    for component in components:
        if component.capitalize() in atomic_masses:
            molecule = molecule.replace(component, component.capitalize())
    return molecule

def parse_molecule(molecule: str):
    """Разбивает молекулу на атомы и их количество."""
    components = re.findall(r'([A-Z][a-z]*)(\d*)', molecule)
    return [(atom, int(count) if count else 1) for atom, count in components]

def calculate_mass(molecule: str):
    """Вычисляет молекулярную массу молекулы."""
    atoms = parse_molecule(molecule)
    return reduce(lambda total, atom: total + atomic_masses.get(atom[0], 0) * atom[1], atoms, 0)

# Приведение молекул к корректному формату
normalized_molecules = map(normalize_molecule, molecules)

# Расчет молярных масс для всех молекул
results = map(lambda mol: (mol, calculate_mass(mol)), normalized_molecules)

# Сортировка по молекулярной массе
sorted_results = sorted(results, key=lambda x: x[1])

# Вывод результата
for molecule, mass in sorted_results:
    print(f"{molecule:<8} {mass:.3f}")
