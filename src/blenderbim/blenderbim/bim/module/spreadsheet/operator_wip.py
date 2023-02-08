import bpy
import pandas

#construct pandas dataframe
#extract ifc data 

def get_ifc_type(self, ifc_product):
    print ('get ifc type')

def get_ifc_building_storey(self, ifc_product):
    print ('get ifc building storey')

def get_ifc_classification_item_and_reference(self, ifc_product):
    print ('get ifc classifcation and reference')

def get_ifc_materials(self, ifc_product):
    print ('get ifc materials')

def get_ifc_properties(self, ifc_product):
    print ('get ifc propetysets and properties')

def get_ifc_quantities(self, ifc_product):
    print ('get ifc quantities')

def get_custom_propertyset(self, ifc_product):
    print ('get ifc custom properties')


class WriteToXLSX(bpy.types.Operator):

    def execute():
        print (' execute')

class FilterIFCElements(bpy.types.Operator):

    def execute():
        print (' execute')

class UnhideIFCElements(bpy.types.Operator):

    def execute():
        print (' execute')

class GetCustomCollection(bpy.types.Operator):

    def execute():
        print (' execute')
