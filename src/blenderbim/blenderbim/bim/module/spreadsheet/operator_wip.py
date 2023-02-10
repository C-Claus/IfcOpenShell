import bpy
import pandas

import ifcopenshell
import ifcopenshell.api
import ifcopenshell.util.element
import ifcopenshell.util.classification

import blenderbim
#import blenderbim.bim.import_ifc
#from blenderbim.bim.ifc import IfcStore

ifc_file_location = "C:\\Algemeen\\07_ifcopenshell\\00_ifc\\02_ifc_library\\IFC Schependomlaan.ifc"

ifc_file = ifcopenshell.open(ifc_file_location)

products = ifc_file.by_type('IfcProduct')




def get_ifc_type(ifc_product):
    
    ifc_type_list = []
    
    if ifc_product: 
        ifcproduct_type = ifcopenshell.util.element.get_type(ifc_product)
        
        if ifcproduct_type:
            ifc_type_list.append(ifcproduct_type.Name)
    
    if not ifc_type_list:
        ifc_type_list.append(None)

    return ifc_type_list


def get_ifc_building_storey(ifc_product):

    building_storey_list = []
        
    spatial_container = ifcopenshell.util.element.get_container(ifc_product)
    
    if spatial_container:    
        building_storey_list.append(spatial_container.Name)
        
    if not building_storey_list:
        building_storey_list.append(None)
         
    return building_storey_list 



def get_ifc_classification_item_and_reference(ifc_product):
    
    classification_list = []

    # Elements may have multiple classification references assigned
    references = ifcopenshell.util.classification.get_references(ifc_product)
    
    if ifc_product:
        for reference in references:
           
            system = ifcopenshell.util.classification.get_classification(reference)
           
            
            classification_list.append(str(system.Name) + ' | ' + str(reference[1]) +  ' | ' + str(reference[2]))
        
    if not classification_list:
        classification_list.append(None)    
    print (classification_list)
    
    
for product in products:
    get_ifc_classification_item_and_reference(ifc_product=product)

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
