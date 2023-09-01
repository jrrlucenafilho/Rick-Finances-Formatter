'''
---------------------------------------------------------------------------------------------------
Reworked version of the calc conversion-and-formatting tool made to help accountants with calc handling/formatting.

Obs: Planned to only work on UNIX-based systems
---------------------------------------------------------------------------------------------------
'''

from re import sub
from os import getcwd, replace
from tabula import convert_into_by_batch
from glob import glob
from pathlib import Path

def main():
    print("Processando os arquivos, por favor espere...")

    #Convert pdfs in input folder using tabula
    convert_into_by_batch(input_dir=(getcwd() + "\calc_input"), output_format="tsv", pages="all", )

    #Change filenames (formats) from tsv to csv
    for tsv_file in glob(getcwd() + "\calc_input\*.tsv"):
        tsv_filename = Path(tsv_file)
        tsv_filename.rename(tsv_filename.with_suffix(".csv"))

    #Add all csvs in the folder to an array
    input_folder = []

    for csv_file in glob(getcwd() + "\calc_input\*.csv"):
        input_folder.append(csv_file)

    for csv_file in input_folder:
        with open(csv_file, 'r', errors="ignore") as file_in:
            file_str = file_in.read()
            file_str = conversion_cleanup(file_str)
            file_in.close()

        with open(csv_file, 'w', errors="ignore") as file_out:
            file_out.write(file_str)
            file_out.close()

    #Move csvs to output folder
    for csv_filepath in glob(getcwd() + "\calc_input\*.csv"):
        replace(csv_filepath, csv_filepath.replace("calc_input", "calc_output"))


def conversion_cleanup(file_str=[str]):
    #Conversion formatting cleanup with regex
    file_str = file_str.replace('\"', '')
    file_str = sub("[\,]{2,}",' ', file_str)
    file_str = sub("[\t]{1,}|[ ]{2,}",';', file_str)

    #Tidying up doc head
    file_str = file_str.replace("Jan;Fev Mar;Abr;Mai;Jun;Jul;Ago Set;Out Nov;Dez;Total", "Jan;Fev;Mar;Abr;Mai;Jun;Jul;Ago;Set;Out;Nov;Dez;Total")
    file_str = file_str.replace("Jan Fev Mar", "Jan;Fev;Mar")
    file_str = file_str.replace("Ago Set", "Ago;Set")
    file_str = file_str.replace("Fev Mar", "Fev;Mar")
    file_str = file_str.replace("Out Nov", "Out;Nov")
    file_str = file_str.replace("Mar Abr Mai", "Mar;Abr;Mai")
    file_str = file_str.replace("Mar Abr", "Mar;Abr")
    file_str = file_str.replace("Matricula:", "\nMatricula:")
    file_str = file_str.replace(";Nome:;", " Nome: ")
    file_str = file_str.replace(";Admis.:", " Admis.:")
    file_str = file_str.replace(";Anuenio.:", " Anuenio.:")
    file_str = file_str.replace(";Opc.FGTS.:;", " Opc.FGTS.: ")
    file_str = file_str.replace(";RS.:", " RS.:")
    file_str = file_str.replace(";Funo", " Funcao")
    file_str = file_str.replace(";Jornada.:;", " Jornada.: ")
    file_str = file_str.replace(";CTPS:;", " CTPS: ")
    file_str = file_str.replace("/;", "/ ")
    file_str = file_str.replace(";Dep", " Dep")
    file_str = file_str.replace(";BCO.:;", " BCO.: ")
    file_str = file_str.replace(";Ag.:", " Ag.:")
    file_str = file_str.replace("CC.:;", "CC.: ")
    file_str = file_str.replace("Referncia", "Referencia")
    file_str = file_str.replace("TIPO DE VERBA:;", "TIPO DE VERBA: ")
    file_str = file_str.replace("Proventos / Desconto", "\nProventos / Desconto")

    #Tidying up provision names
    file_str = file_str.replace("Salrio", "Salario")
    file_str = file_str.replace("Anunio", "Anuenio")
    file_str = file_str.replace("Gratificao de Funo Conv.", "Gratificacao de Funcao Conv.")
    file_str = file_str.replace("Hora Extra70% - Norm", "Hora Extra 70% - Norm")
    file_str = file_str.replace("Gratificacao Natal", "Gratificacao Natal")
    file_str = file_str.replace("Frias", "Ferias")
    file_str = file_str.replace("Abono Pecunirio", "Abono Pecuniario")
    file_str = file_str.replace("Mdia Proventos", "Media Proventos")
    file_str = file_str.replace("Gratificao", "Gratificacao")
    file_str = file_str.replace("Incorporao", "Incorporacao")
    file_str = file_str.replace("Funo", "Função")
    file_str = file_str.replace("Alimentao", "Alimentacao")
    file_str = file_str.replace(";70%", " 70%")
    
    #Tidying up description names
    file_str = file_str.replace("Lquido", "Liquido")
    file_str = file_str.replace("Contribuio", "Contribuicao")

    return file_str

#TODO: Add transpose feature
#def transpose(file_str = [str]):
'''

'''

if __name__ == "__main__":
    main()