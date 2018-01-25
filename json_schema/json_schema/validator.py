import types, sys, re,copy

__all__ = ['JSONSchemaValidator']

class JSONSchemaValidator:
	'''
	Implementation of the json-schema validator
	'''
	# Map of schema types to their equivalent in the python types module
	