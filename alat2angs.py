import re

def read_input_file(filename):
    """ Reads the Quantum ESPRESSO input file and extracts alat and CELL_PARAMETERS. """
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    alat_bohr = None
    cell_parameters_alat = []
    reading_cell_parameters = False
    
    for line in lines:
        if "CELL_PARAMETERS" in line:
            match = re.search(r"alat=\s*([0-9\.]+)", line)
            if match:
                alat_bohr = float(match.group(1))
            reading_cell_parameters = True
            continue
        
        if reading_cell_parameters:
            if line.strip():
                cell_parameters_alat.append(list(map(float, line.split())))
            if len(cell_parameters_alat) == 3:
                break
    
    if alat_bohr is None or len(cell_parameters_alat) != 3:
        raise ValueError("Error: Could not find alat or CELL_PARAMETERS correctly in file.")
    
    return alat_bohr, cell_parameters_alat

def convert_alat_to_angstrom(alat_bohr, cell_parameters_alat):
    """ Converts the values ​​in the CELL_PARAMETERS array from alat units to angstroms. """
    BOHR_TO_ANGSTROM = 0.529177
    alat_angstrom = alat_bohr * BOHR_TO_ANGSTROM
    return [[val * alat_angstrom for val in row] for row in cell_parameters_alat]

def main():
    input_file = input("Enter the input file name: ")
    try:
        alat_bohr, cell_parameters_alat = read_input_file(input_file)
        cell_parameters_angstrom = convert_alat_to_angstrom(alat_bohr, cell_parameters_alat)
        
        print("\nCELL_PARAMETERS angstrom")
        for row in cell_parameters_angstrom:
            print(" ".join(f"{val:.9f}" for val in row))
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
