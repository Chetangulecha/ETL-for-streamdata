import pandas as pd
import numpy as np
import xml.dom.minidom as parser

import etlUtils

def mapping_function(value, mapping_dict) : 
    
    if value in mapping_dict: 
        return mapping_dict[value]
    return value

def perform_mapping(transformation, data_source_map, transformed_data) :
    
    #take input data from sources and already existing transformed data
    input_dict = dict()
    inputs = transformation.getElementsByTagName('input')
    input_feilds, input_dict = etlUtils.get_input_data(inputs, data_source_map, transformed_data, input_dict)

    data = input_dict[input_feilds[0]]
    

    #create maps
    mapping_list = transformation.getElementsByTagName('map')
    mapping_dict = dict()
    for mapping in mapping_list : 
        key = mapping.getElementsByTagName('from')[0].childNodes[0].data
        value = mapping.getElementsByTagName('to')[0].childNodes[0].data
        if value == 'NaN' : 
            value = None
        mapping_dict[key] = value
    #conditional_data = list(zip(data, conditions))
    mapped_data = np.array(list(map(lambda value : mapping_function(value, mapping_dict) , data.tolist())))

    #form output from existing transormed data
    outputs = transformation.getElementsByTagName('output')
    transformed_data = etlUtils.register_output_data(outputs, mapped_data, transformed_data)    
    return transformed_data

def evaluate_expression(expression, input_dict) : 
    expression = expression + ' '
    
    def precedence(op):      
        if op == '+' or op == '-':
            return 1
        if op == '*' or op == '/':
            return 2
        return 0
        
    def applyOp(a, b, op):        
        if op == '+': return a + b
        if op == '-': return a - b
        if op == '*': return a * b
        if op == '/': return a / b

    values = [] #stack to store values
    ops = [] #stack to store operations
    i = 0
    tokens = expression
    while i < len(tokens):
        #skip on white space
        if tokens[i] == ' ':
            i += 1
            continue
         
        elif tokens[i] == '(':
            ops.append(tokens[i])
         
        elif tokens[i] == '#':
            pos = i+tokens[i:].index(' ')
            val = float(tokens[i+1 : pos])
            values.append(val)
            i=pos

        elif tokens[i] == '@':
            pos = i+tokens[i:].index(' ')
            input_var = tokens[i+1:pos]
            values.append(input_dict[input_var].astype(np.float))
            i=pos

        elif tokens[i] == ')':
            while len(ops) != 0 and ops[-1] != '(':
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                values.append(applyOp(val1, val2, op))
            ops.pop()

        else:
            while (len(ops) != 0 and
                precedence(ops[-1]) >=  precedence(tokens[i])):
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                values.append(applyOp(val1, val2, op))
            ops.append(tokens[i])
        i += 1
    
    while len(ops) != 0:
        val2 = values.pop()
        val1 = values.pop()
        op = ops.pop()
        values.append(applyOp(val1, val2, op))

    return values[-1]


def perform_conversion(transformation, data_source_map, transformed_data) :
    conversion_list = etlUtils.getChildElements(transformation)    
    for conversion in conversion_list : 
        if conversion._get_tagName() == 'formula' :
            input_dict = dict()
            inputs = conversion.getElementsByTagName('input')
            input_feilds, input_dict = etlUtils.get_input_data(inputs, data_source_map, transformed_data, input_dict)
            expression = conversion.getElementsByTagName('expression')[0].childNodes[0].data
            evaluated_val = evaluate_expression(expression, input_dict)
            outputs = conversion.getElementsByTagName('output')
            transformed_data = etlUtils.register_output_data(outputs, evaluated_val, transformed_data)
        elif conversion._get_tagName() == 'floor' :
            input_dict = dict()
            inputs = conversion.getElementsByTagName('input')
            input_feilds, input_dict = etlUtils.get_input_data(inputs, data_source_map, transformed_data, input_dict)
            floored_val = np.floor(input_dict[input_feilds[0]])
            outputs = conversion.getElementsByTagName('output')
            transformed_data = etlUtils.register_output_data(outputs, floored_val, transformed_data)
        elif conversion._get_tagName() == 'ceil' :
            input_dict = dict()
            inputs = conversion.getElementsByTagName('input')
            input_feilds, input_dict = etlUtils.get_input_data(inputs, data_source_map, transformed_data, input_dict)
            ceiled_val = np.ceil(input_dict[input_feilds[0]])
            outputs = conversion.getElementsByTagName('output')
            transformed_data = etlUtils.register_output_data(outputs, ceiled_val, transformed_data)
        elif conversion._get_tagName() == 'power' :
            input_dict = dict()
            inputs = conversion.getElementsByTagName('input')
            input_feilds, input_dict = etlUtils.get_input_data(inputs, data_source_map, transformed_data, input_dict)
            power = float(conversion.getElementsByTagName('power-value')[0].childNodes[0].data)
            pow_val = np.power(input_dict[input_feilds[0]],power)
            outputs = conversion.getElementsByTagName('output')
            transformed_data = etlUtils.register_output_data(outputs, pow_val, transformed_data)
        else :
            break
    return transformed_data


def perform_lookup(transformation, data_source_map, transformed_data):
    #take input data from sources and already existing transformed data
    input_dict = dict()
    inputs = transformation.getElementsByTagName('input')
    input_feilds, input_dict = etlUtils.get_input_data(inputs, data_source_map, transformed_data, input_dict)
    
    
    lookup = transformation.getElementsByTagName('lookup-source')[0]
    
    lookup_key_dict = dict()
    lookup_key =  lookup.getElementsByTagName('source-key')[0].getElementsByTagName('input')
    lookup_key_feilds, lookup_key_dict = etlUtils.get_input_data(lookup_key, data_source_map, transformed_data, lookup_key_dict)

    lookup_value_dict = dict()
    lookup_value = lookup.getElementsByTagName('source-value')[0].getElementsByTagName('input')
    lookup_value_feilds, lookup_value_dict = etlUtils.get_input_data(lookup_value, data_source_map, transformed_data, lookup_value_dict)

    lookup_dict = dict(zip(lookup_key_dict[lookup_key_feilds[0]], lookup_value_dict[lookup_value_feilds[0]]))
    data = input_dict[input_feilds[0]]
    mapped_data = np.array(list(map(lambda value : mapping_function(value, lookup_dict) , data.tolist())))

    #form output from existing transormed data
    outputs = transformation.getElementsByTagName('output')
    transformed_data = etlUtils.register_output_data(outputs, mapped_data, transformed_data)    
    return transformed_data

def perform_merging(transformation, data_source_map, transformed_data):
    input_dict = dict()
    inputs = transformation.getElementsByTagName('input')
    input_feilds, input_dict = etlUtils.get_input_data(inputs, data_source_map, transformed_data, input_dict)

    merged_data = np.append(input_dict[input_feilds[0]],input_dict[input_feilds[1]])
    for idx in range(2, len(input_feilds)) : 
        merged_data = np.append(merge_data, input_dict[input_feilds[idx]])
    outputs = transformation.getElementsByTagName('output')
    transformed_data = etlUtils.register_output_data(outputs, merged_data, transformed_data)    
    return transformed_data


def perform_transformation(transformation_list, data_source_map) : 
    transformed_data = dict()
    for transformation in transformation_list : 
        if transformation._get_tagName() == 'mapping' :
            transformed_data = perform_mapping(transformation, data_source_map, transformed_data)
        elif transformation._get_tagName() == 'conversion' :
            transformed_data = perform_conversion(transformation, data_source_map, transformed_data)
        elif transformation._get_tagName() == 'lookup' :
            transformed_data = perform_lookup(transformation, data_source_map, transformed_data)
        elif transformation._get_tagName() == 'merge' :
            transformed_data = perform_merging(transformation, data_source_map, transformed_data)
        else : 
            print('Transformation[{}] not supported'.format(transformation._get_tagName()))
    return transformed_data
