import yaml
import os
import json
import joblib
import numpy as np


params_path = 'params.yaml'
scehema_path = os.path.join('prediction_service', 'schema_in.json')

class NotInRange(Exception):
    def __init__(self, message='Values entered are not in range'):
        self.message = message
        super().__init__(self.message)

class NotInCols(Exception):
    def __init__(self, message='Not in columns'):
        self.message = message
        super().__init__(self.message)


def read_yaml(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def prediction(data):
    config  = read_yaml(params_path)
    model_dir_path = config['webapp_model_dir']
    model = joblib.load(model_dir_path)
    prediction = model.predict(data).tolist()[0]
    try:
        if 3 <= prediction >= 0: 
            return np.round(prediction, 3)
        else:
            raise NotInRange
    except:
        return "Unexpected result"


def get_schema(schema_path = scehema_path):
    with open(schema_path) as json_file:
        config = json.load(json_file)
    return config


def validate_inputs(dict_request):
    def _validate_cols(cols):
        schema = get_schema()
        actual_cols = schema.keys()
        if cols not in actual_cols:
            raise NotInCols

    def _validate_values(cols):
        schema = get_schema()
        if not (schema[cols]['min'] <= float(dict_request[cols]) <= schema[cols]['max']):
            raise NotInRange

    for cols, values in dict_request.items():
        _validate_cols(cols)
        _validate_values(cols) 
    return True

def form_response(dict_request):
    if validate_inputs(dict_request):
        data = dict_request.values()
        data = [list(map(float, data))]
        response = prediction(data)
        return response


def api_response(dict_request):
    try:
        if validate_inputs(dict_request):
            data = np.array([list(dict_request.values())])
            response = prediction(data)
            response = {'response': response}
    except Exception as e:
        response = {'the expected_range': get_schema(), 'response':str(e)}
        return response
