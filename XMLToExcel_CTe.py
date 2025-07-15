import xml.etree.ElementTree as ET
import os
from datetime import datetime

xml_folder = r'C:\Users\ESCARIZ\Desktop\XML_testes'
ns = {
    'cte': 'http://www.portalfiscal.inf.br/cte',
    'ds': 'http://www.w3.org/2000/09/xmldsig#'
}

timeNow = datetime.today().strftime("%d-%m-%Y_%H-%M-%S")

def transform_toma(toma_value):
    if toma_value == '0':
        return 'remetente'
    elif toma_value == '1':
        return 'destinatário'
    else:
        return 'desconhecido'  # unknown or other cases

fields = {
    'Id': './/cte:infCte',
    'xNome': './/cte:emit/cte:xNome',
    'dhEmi': './/cte:ide/cte:dhEmi',
    'nCT': './/cte:ide/cte:nCT',
    'chCTe': './/cte:protCTe/cte:infProt/cte:chCTe',
    'vRec': './/cte:vPrest/cte:vRec',
    'dPrev': './/cte:compl/cte:ObsCont[@xCampo="dPrev"]/cte:xTexto',
    'toma_num': './/cte:ide/cte:toma3/cte:toma'
}

xml_lst = [f for f in os.listdir(xml_folder) if f.lower().endswith('.xml')]
nameCSV = 'transporte_CTE' + timeNow + '.csv'

with open(nameCSV, 'w', encoding='utf-8') as f_out:
    # add new columns for toma number and description
    header = list(fields.keys()) + ['toma_desc', 'filename']
    f_out.write(','.join(header) + '\n')

    for xml_file in xml_lst:
        xml_path = os.path.join(xml_folder, xml_file)

        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()

            values = []
            toma_value = ''

            for key, path in fields.items():
                elem = root.find(path, ns)
                if key == 'Id':
                    val = elem.attrib.get('Id') if elem is not None else ''
                else:
                    val = elem.text.strip() if elem is not None and elem.text else ''

                # Save toma value to use for description later
                if key == 'toma_num':
                    toma_value = val

                # Keep chCTe value quoted to preserve leading zeros
                if key == 'chCTe' and val:
                    val = f"'{val}'"

                values.append(val)

            # Transform toma number into descriptive text
            toma_desc = transform_toma(toma_value)
            values.append(toma_desc)

            values.append(xml_file)
            f_out.write(','.join(values) + '\n')

        except ET.ParseError:
            print(f"❌ Failed to parse {xml_file}")
        except Exception as e:
            print(f"⚠️ Error processing {xml_file}: {e}")
