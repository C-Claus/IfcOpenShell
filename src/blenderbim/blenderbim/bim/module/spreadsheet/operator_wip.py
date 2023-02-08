import bpy
import pandas
import ifcopenshell.api
#import blenderbim
#import blenderbim.bim.import_ifc
#from blenderbim.bim.ifc import IfcStore


def get_ifc_type(self, ifc_product):
    print ('get ifc type')

    ifc_type_list = []
    
    if ifc_product: 
        ifcproduct_type = ifcopenshell.util.element.get_type(ifc_product)
        
        if ifcproduct_type:
            ifc_type_list.append(ifcproduct_type.Name)
    
    if not ifc_type_list:
        ifc_type_list.append(None)

    
    return ifc_type_list

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

def get_ifc_custom_propertyset(self, ifc_product):
    print ('get ifc custom properties')


class ConstructPandasDataFrame(bpy.types.Operator):

    def execute():
        print (' execute')
class WriteToXLSX(bpy.types.Operator):

    def execute():
        print (' execute')

class WriteToODS(bpy.types.Operator):

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
