ruta_file=GetVar('ruta_file')
#ruta_file=r"C:\AD\AperturaDeCuentas-BMSC\DataExtraida\34-MARIOLY PAZ NUNEZ-Cuenta de Ahorro-BENI-10166\data.xlsx"
wb = load_workbook(ruta_file, data_only=True)
data = wb["Hoja1"]
variables = GetVar('variables')
variables = variables.replace("[","")
variables = variables.replace("]","")
variables = variables.split(sep=",")
print(variables)
for var in variables:
  i=1
  while i<1000:
    #print(data[f'C{i}'].value)
    if data[f'A{i}'].value == var:
      if data[f'C{i}'].value != None:
        SetVar(var,data[f'C{i}'].value)
      i=1000
    i=i+1