import xmlschema;
from pandas import notna
import xmltodict
from app.file_operations import FileOperations
import json

class Converter:

    def convert_xml_to_json(xml_document:str, schema: str) -> dict:
        xs = xmlschema.XMLSchema(schema)
        result = xs.to_dict(xml_document)
        return result
    
    def convert_xml_to_dict(xml_document_path:str) -> dict:
        loaded_data = FileOperations.open_file(xml_document_path)
        result = xmltodict.parse(loaded_data, xml_attribs=False)
        return result
    
    def convert_xls_to_classification_json(xls_raw: dict, classification_code: str, classification_name: dict) -> dict:
        result = {"code": classification_code,
                  "name": classification_name,
                  "elements":[]}
        elements_count = len(xls_raw['code'])
        for i in range(0, elements_count):  
            element = {'code': '','name':{}}
            for x, y in xls_raw.items():
                if notna(y[i]):
                    if x == 'code':
                        element['code'] = str(y[i])
                    if x == 'name_ET':
                        element['name'].update({'et': y[i]})
                    elif x == 'name_EN':
                        element['name'].update({'en': y[i]})
                    elif x == 'validFromDate':
                        element['valid_from_date'] = str(y[i].date())[:10]
                    # add all other fields in table
                    # else:
                    #     # element[x] = y[i]
            result["elements"].append(element)
        return result
    
    def clear_string (sentence: str) -> str:
        return sentence.replace("(", " (").replace("  ", " ").replace(u"\u00A0", "")
    
    def make_element_code_and_name_pairs (list_of_codes: str, classification_code: str) -> dict:
        codes = [s.strip() for s in list_of_codes.split((","))]
        file_name = "JSON_files/export/" + classification_code + ".json"
        element_pairs = {}
        with open(file_name, "r") as read_content: 
            json_object = json.load(read_content)
            elements = json_object['elements']
            for k in elements:
                if k['code'] in codes:
                    element_pairs[k['code']] = k['name']['et']
        return element_pairs

    def convert_xls_to_subaccount_limitations_json(xls_raw: dict) -> dict:
        result = {"limitations":[]}
        elements_count = len(xls_raw['code'])
        for i in range(0, elements_count):  
            element = {'accountMainID': str(xls_raw['code'][i]), 'name':{}, 'subAccounts':{}}
            for x, y in xls_raw.items():
                if notna(y[i]):
                    if x == 'name_ET':
                        element['name'].update({'et': Converter.clear_string(y[i])})
                    elif x == 'MUUTUSELIIK2024ap':
                        if y[i] == 'all':
                            element['subAccounts'].update({'MUUTUSELIIK2024ap': {}})
                        else:
                            element['subAccounts'].update({'MUUTUSELIIK2024ap': Converter.make_element_code_and_name_pairs(y[i], "MUUTUSELIIK2024ap")})
                    elif x == 'ANDMETEESITLUSVIIS2024ap':
                        if y[i] == 'all':
                            element['subAccounts'].update({'ANDMETEESITLUSVIIS2024ap': {}})
                        else:
                            element['subAccounts'].update({'ANDMETEESITLUSVIIS2024ap': Converter.make_element_code_and_name_pairs(y[i], "ANDMETEESITLUSVIIS2024ap")})
                    elif x.strip() == 'RTK2T2013ap':
                        if y[i] == 'all':
                            element['subAccounts'].update({'RTK2T2013ap': {}})
                        else:
                            element['subAccounts'].update({'RTK2T2013ap': Converter.make_element_code_and_name_pairs(y[i], "RTK2T2013ap")})
                    elif x == 'EMTAK2008ap':
                        if y[i] == 'all':
                            element['subAccounts'].update({'EMTAK2008ap': {}})
                        else:
                            element['subAccounts'].update({'EMTAK2008ap': Converter.make_element_code_and_name_pairs(y[i], "EMTAK2008ap")})
                    elif x == 'VARAGRUPP2024ap':
                        if y[i] == 'all':
                            element['subAccounts'].update({'VARAGRUPP2024ap': {}})
                        else:
                            element['subAccounts'].update({'VARAGRUPP2024ap': Converter.make_element_code_and_name_pairs(y[i], "VARAGRUPP2024ap")})
                    elif x == 'SEOTUDOSAPOOL2024ap':
                        if y[i] == 'all':
                            element['subAccounts'].update({'SEOTUDOSAPOOL2024ap': {}})
                        else:
                            element['subAccounts'].update({'SEOTUDOSAPOOL2024ap': Converter.make_element_code_and_name_pairs(y[i], "SEOTUDOSAPOOL2024ap")})
            result["limitations"].append(element)
        return result

