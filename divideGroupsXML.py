import xml.etree.ElementTree as ET
from pathlib import Path
import json
import re

def DivideGroups():
    # Namespace usado em NF-e
    NS = {
        'nfe': 'http://www.portalfiscal.inf.br/nfe'
    }

    # CFOPs válidos para continuar na pasta "55"
    CFOP_VALIDOS = {'6101', '5101', '6102', '5102', '5917', '6917', '5113', '6113', '5114', '6114','5405','6910','6115','6105'}

    def extract_info(xml_path):
        """Parse XML and extract mod, chNFe or Id, CFOP, XML root, and dict."""
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Extract mod
        mod_elem = root.find('.//nfe:mod', NS)
        mod_value = mod_elem.text.strip() if mod_elem is not None else "unknown"

        # Try to extract chNFe
        chNFe_elem = root.find('.//nfe:protNFe/nfe:infProt/nfe:chNFe', NS)
        if chNFe_elem is not None and chNFe_elem.text:
            file_id = chNFe_elem.text.strip()
        else:
            # Fallback: extract Id from infNFe and isolate digits
            infNFe_elem = root.find('.//nfe:infNFe', NS)
            if infNFe_elem is not None:
                id_attr = infNFe_elem.attrib.get('Id', '')
                digits_only = ''.join(re.findall(r'\d+', id_attr))
                file_id = digits_only if digits_only else f"no_id_{xml_path.stem}"
            else:
                file_id = f"no_id_{xml_path.stem}"

        # Extract CFOP
        cfop_elem = root.find('.//nfe:det/nfe:prod/nfe:CFOP', NS)
        cfop_value = cfop_elem.text.strip() if cfop_elem is not None else None

        # Extract content into dict
        record = root.find('.//nfe:infNFe', NS)
        record_dict = {}
        if record is not None:
            for child in record:
                tag = child.tag.split('}', 1)[-1]
                record_dict[tag] = {}
                for sub in child:
                    sub_tag = sub.tag.split('}', 1)[-1]
                    record_dict[tag][sub_tag] = sub.text.strip() if sub.text else None

        return mod_value, file_id, cfop_value, root, record_dict

    def process_folder(input_folder, output_base):
        input_folder = Path(input_folder)
        output_base = Path(output_base)
        output_base.mkdir(exist_ok=True)

        for xml_file in input_folder.glob("*.xml"):
            mod, file_id, cfop, xml_root, json_data = extract_info(xml_file)

            # Redirecionamento com base no CFOP para mod 55
            if mod == '55' and cfop not in CFOP_VALIDOS:
                mod = "unknown"

            # Define pasta de saída
            mod_folder = output_base / mod
            mod_folder.mkdir(exist_ok=True)

            # Sanitize file_id
            filename = "".join(c for c in file_id if c.isalnum() or c in ('-', '_'))

            # Caminhos finais
            xml_out = mod_folder / f"{filename}.xml"
            #json_out = mod_folder / f"{filename}.json"

            # Salvar XML
            ET.ElementTree(xml_root).write(xml_out, encoding="utf-8", xml_declaration=True)

            # Salvar JSON
           #with open(json_out, "w", encoding="utf-8") as f:
               #json.dump(json_data, f, ensure_ascii=False, indent=2)

    # === Example Usage ===
    process_folder(
        input_folder=r"C:\Users\ESC-CMO13\Desktop\downloadXML\XMLs\attachments",
        output_base="xml_output"
    )