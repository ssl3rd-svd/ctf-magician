from cmag.project.config import CMagFieldTypes as fieldtypes

class plugins(fieldtypes.abspathlist):
    name = 'plugins'
    desc = 'External plugins path.'

CMagProjectConfigFields = [plugins]