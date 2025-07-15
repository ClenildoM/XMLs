import xml.etree.ElementTree as ET
import os
from datetime import datetime

# Path to folder with XML files
xml_folder = r'C:\Users\ESC-CMO13\Desktop\downloadXML\XMLs\xml_output\55'

# Define the XML namespace
ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

# Current timestamp for filename
timeNow = datetime.today().strftime("%d-%m-%Y_%H-%M-%S")

# Fields to extract
fields = {
    'Id': './/nfe:infNFe',           # attribute
    'xNome': './/nfe:emit/nfe:xNome',
    'dhEmi': './/nfe:ide/nfe:dhEmi',
    'nNF': './/nfe:ide/nfe:nNF',
    'chNFe': './/nfe:protNFe/nfe:infProt/nfe:chNFe',
    'cfop': './/nfe:det/nfe:prod/nfe:CFOP'
}

# Get list of XML files
xml_lst = [f for f in os.listdir(xml_folder) if f.lower().endswith('.xml')]
nameCSV = 'NFe_distribuidoras' + timeNow + '.csv'

# Open CSV for writing
with open(nameCSV, 'w', encoding='utf-8') as f_out:
    # Write header (fields + filename)
    f_out.write(','.join(list(fields.keys()) + ['filename']) + '\n')

    for xml_file in xml_lst:
        xml_path = os.path.join(xml_folder, xml_file)

        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()

            values = []
            for key, path in fields.items():
                elem = root.find(path, ns)
                if key == 'Id':
                    val = elem.attrib.get('Id') if elem is not None else ''
                else:
                    val = elem.text.strip() if elem is not None and elem.text else ''

                if key == 'chNFe' and val:
                    val = f"'{val}'"

                values.append(val)

            # Add filename as last column
            values.append(xml_file)

            # Write row
            f_out.write(','.join(values) + '\n')

        except ET.ParseError:
            print(f"❌ Failed to parse {xml_file}")
        except Exception as e:
            print(f"⚠️ Error processing {xml_file}: {e}")
