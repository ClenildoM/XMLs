import xml.etree.ElementTree as ET
import os
from datetime import datetime
import pandas as pd

def ToExcel():
    xml_folder = r'dist\xml_output\55'
    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    #timeNow = datetime.today().strftime("%d-%m-%Y_%H-%M-%S")

    fields = {
        'Id': './/nfe:infNFe',
        'Nome': './/nfe:emit/nfe:xNome',
        'Emissao': './/nfe:ide/nfe:dhEmi',
        'NF': './/nfe:ide/nfe:nNF',
        'ChaveNF': './/nfe:protNFe/nfe:infProt/nfe:chNFe',
        'CFOP': './/nfe:det/nfe:prod/nfe:CFOP',
        'Serie' : './/nfe:ide/nfe:serie'
    }

    xml_lst = [f for f in os.listdir(xml_folder) if f.lower().endswith('.xml')]
    dados = []

    for xml_file in xml_lst:
        xml_path = os.path.join(xml_folder, xml_file)

        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()

            values = {}
            for key, path in fields.items():
                elem = root.find(path, ns)
                if key == 'Id':
                    val = elem.attrib.get('Id') if elem is not None else ''
                else:
                    val = elem.text.strip() if elem is not None and elem.text else ''

                if key == 'ChaveNF' and val:
                    val = f"'{val}'"

                values[key] = val
            dados.append(values)

        except ET.ParseError:
            print(f"❌ Failed to parse {xml_file}")
        except Exception as e:
            print(f"⚠️ Error processing {xml_file}: {e}")

    # Exportar com pandas
    df = pd.DataFrame(dados)
    return df
   # df.to_excel('NFe_distribuidoras.xlsx', index=False)
