import xml.dom.minidom as parser

def getChildElements(node) :
    childNodes = node.childNodes
    childNodes_list = []
    for childNode in  childNodes : 
        if isinstance(childNode, parser.Element) : 
            childNodes_list.append(childNode)
    return childNodes_list

def get_input_data(inputs, data_source_map, transformed_data, input_data) : 
    '''
    --------------INPUT--------------------------
    input : list of input elements
    data_source_map : map containing all data from extract operation
    transformed_data : map containing intermediate data for transformation
    input_data : dict in which input data needs to be populated
    -------------OUTPUT---------------------------
    input_fields : list of combination of sourceId and inputId
    input_data : data as per the content of input fields
    '''
    input_feilds = []
    for input_feild in inputs : 
        feild_name = input_feild.childNodes[0].data
        source_id = input_feild.getAttribute('sourceId')
        input_id = input_feild.getAttribute('inputId')
        if source_id == '' :
            input_feilds.append(input_id) 
            input_data[input_id] = transformed_data[feild_name]
        else :
            input_feilds.append(input_id)
            df = data_source_map[source_id]
            input_data[input_id] = df[feild_name]
    return input_feilds, input_data

def register_output_data(outputs, output_data, transformed_data) : 
    for output_feild in outputs : 
        output_id = output_feild.getAttribute('outputId')
        transformed_data[output_id] = output_data
    return transformed_data

# def perform_condition() : 
#     input_dict = dict()
#     inputs = transformation.getElementsByTagName('input')
#     input_feilds, input_dict = etlUtils.get_input_data(inputs, data_source_map, transformed_data, input_dict)
    
