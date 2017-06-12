'''
Created on Dec 13, 2016

@author: joseph
'''
from enum import Enum
import copy


class InvalidValidationState(Exception):
    pass


class ValidationState(Enum):
    SUCCESS = 0
    INVALID = 1
    UNSPEC = 2


class Validator():
    pass


class ParameterValidator(Validator):
    parameters_required = []
    safetoskip_params = []
    err_responses = {'unspecified': {'status': 'ERROR',
                                     'error': 'NO_%s_SPECIFIED'},
                     'invalid': {'status': 'INVALID',
                                 'error': 'INVALID_VALUE_FOR_%s'}
                     }

    def _process_error(self, typ, param=None):
        if typ is ValidationState.INVALID:
            response = copy.deepcopy(self.err_responses['invalid'])
            response['error'] = response['error'] % (param)
        elif typ is ValidationState.UNSPEC:
            response = copy.deepcopy(self.err_responses['unspecified'])
            response['error'] = response['error'] % (param)
        else:
            raise InvalidValidationState()
        return response

    def validate(self, params):
        cleaned_params = []
        for required_parameter, is_valid in self.parameters_required:
            if required_parameter in params:
                try:
                    cleaned_params.append(
                        (required_parameter,
                         is_valid(params[required_parameter])
                         if is_valid is not None else
                         params[required_parameter]))
                except:
                    return self._process_error(
                        ValidationState.INVALID, required_parameter), None
            elif required_parameter not in self.safetoskip_params:
                return self._process_error(
                    ValidationState.UNSPEC, required_parameter), None
        return None, dict(cleaned_params)
