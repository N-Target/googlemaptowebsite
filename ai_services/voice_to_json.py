"""
Voice to JSON Editor - Convert voice input to structured JSON
"""

import json
import re

class VoiceToJSON:
    def __init__(self):
        self.field_patterns = {
            'name': r'(?:my name is|i am|name:?)\s+([a-zA-Z\s]+)',
            'email': r'(?:email is|email:?)\s+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
            'phone': r'(?:phone|number|call me at):?\s*([\d\s\-\+\(\)]+)',
            'message': r'(?:message is|i want to say|tell them):?\s*(.+)',
            'service': r'(?:interested in|looking for|need):?\s*([a-zA-Z\s]+)',
        }
    
    def parse_voice_input(self, text):
        """
        Parse voice input and extract structured data
        """
        text = text.lower().strip()
        result = {}
        
        # Extract fields using patterns
        for field, pattern in self.field_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                result[field] = match.group(1).strip()
        
        # Clean up phone numbers
        if 'phone' in result:
            result['phone'] = re.sub(r'[^\d+]', '', result['phone'])
        
        return result
    
    def text_to_contact_form(self, text):
        """
        Convert natural language to contact form JSON
        """
        data = self.parse_voice_input(text)
        
        contact_form = {
            'name': data.get('name', ''),
            'email': data.get('email', ''),
            'phone': data.get('phone', ''),
            'message': data.get('message', ''),
            'service_interest': data.get('service', ''),
            'source': 'voice_input',
            'timestamp': None  # Will be set by server
        }
        
        return contact_form
    
    def validate_contact_data(self, data):
        """
        Validate contact form data
        """
        errors = []
        
        if not data.get('name'):
            errors.append('Name is required')
        
        email = data.get('email', '')
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if email and not re.match(email_pattern, email):
            errors.append('Invalid email format')
        
        if not data.get('email') and not data.get('phone'):
            errors.append('Either email or phone is required')
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'data': data
        }
    
    def create_json_schema(self, form_type='contact'):
        """
        Generate JSON schema for different form types
        """
        schemas = {
            'contact': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'minLength': 2},
                    'email': {'type': 'string', 'format': 'email'},
                    'phone': {'type': 'string'},
                    'message': {'type': 'string'},
                    'service_interest': {'type': 'string'}
                },
                'required': ['name']
            },
            'booking': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'email': {'type': 'string', 'format': 'email'},
                    'phone': {'type': 'string'},
                    'service': {'type': 'string'},
                    'date': {'type': 'string', 'format': 'date'},
                    'time': {'type': 'string'},
                    'notes': {'type': 'string'}
                },
                'required': ['name', 'email', 'service', 'date']
            }
        }
        
        return schemas.get(form_type, schemas['contact'])

if __name__ == "__main__":
    # Test
    voice_json = VoiceToJSON()
    
    test_input = "My name is John Doe, email is john@example.com, phone is +36 30 123 4567, and I'm interested in haircut services"
    
    result = voice_json.text_to_contact_form(test_input)
    print("Parsed contact form:")
    print(json.dumps(result, indent=2))
    
    validation = voice_json.validate_contact_data(result)
    print("\nValidation result:")
    print(json.dumps(validation, indent=2))
