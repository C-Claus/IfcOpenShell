import bpy
import pandas
import collections
from collections import defaultdict

import ifcopenshell
import ifcopenshell.api
import ifcopenshell.util.element
import ifcopenshell.util.classification
#import ifcopenshell.util.material

import blenderbim
#import blenderbim.bim.import_ifc
#from blenderbim.bim.ifc import IfcStore

import pandas as pd

ifc_file_location = "C:\\Algemeen\\07_ifcopenshell\\00_ifc\\02_ifc_library\\IFC Schependomlaan.ifc"
#ifc_file_location = "C:\\Algemeen\\07_ifcopenshell\\00_ifc\\02_ifc_library\\IFC4 demo.ifc"
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
          
    return (classification_list)
    
    
def get_ifc_materials(ifc_product):
    
    material_list = []
     
    if ifc_product:
        ifc_material = ifcopenshell.util.element.get_material(ifc_product)
        if ifc_material:
            
            if ifc_material.is_a('IfcMaterial'):
                material_list.append(ifc_material.Name)
            
            if ifc_material.is_a('IfcMaterialList'):
                for materials in ifc_material.Materials:
                   material_list.append(materials.Name)
            
            if ifc_material.is_a('IfcMaterialConstituentSet'):
                for material_constituents in ifc_material.MaterialConstituents:
                    material_list.append(material_constituents.Material.Name)
            
            if ifc_material.is_a('IfcMaterialLayerSetUsage'):
                for material_layer in ifc_material.ForLayerSet.MaterialLayers:
                    material_list.append(material_layer.Material.Name)
                
            if ifc_material.is_a('IfcMaterialProfileSetUsage'):
                for material_profile in (ifc_material.ForProfileSet.MaterialProfiles):
                    material_list.append(material_profile.Material.Name)
    
    if not material_list:
        material_list.append(None)
        
    return material_list
    

def get_ifc_properties(ifc_product):
    #print ('get ifc propetysets and properties')
    
    property_set_common_list = []
    property_name = 'IsExternal'
    
    #IsExternal
    #LoadBearing
    #FireRating
    #AcousticRating
    #Compartmentation
    
    #netside_area = ifcopenshell.util.element.get_pset(ifc_product, "Pset_WallCommon","IsExternal")
    
    if ifc_product:
        if ifc_product.IsDefinedBy:
            for ifc_reldefinesbyproperties in ifc_product.IsDefinedBy:
                if ifc_reldefinesbyproperties.is_a() == 'IfcRelDefinesByProperties':
                    if ifc_reldefinesbyproperties.RelatingPropertyDefinition.is_a() == 'IfcPropertySet':
                        if (ifc_reldefinesbyproperties.RelatingPropertyDefinition.Name).startswith('Pset_') and (ifc_reldefinesbyproperties.RelatingPropertyDefinition.Name).endswith('Common'):
                            for ifc_property in ifc_reldefinesbyproperties.RelatingPropertyDefinition.HasProperties:
                                
                                if ifc_property.Name == property_name:
                                    if ifc_property.NominalValue:
                                        property_set_common_list.append(ifc_property.NominalValue[0])
                                        
    if not property_set_common_list:
        property_set_common_list.append(None)
        

    return (property_set_common_list)                                   


def get_ifc_quantities(ifc_product):
  
    quantity_list  = []
    
    if ifc_product:
        quantity_list.append(ifcopenshell.util.element.get_pset(ifc_product, "BaseQuantities","Area"))
        quantity_list.append(ifcopenshell.util.element.get_pset(ifc_product, "BaseQuantities","NetArea"))
        quantity_list.append(ifcopenshell.util.element.get_pset(ifc_product, "BaseQuantities","NetSideArea"))
        
    if not quantity_list:
        quantity_list.append(None)
    
    
    return quantity_list


def get_ifc_custom_propertyset(ifc_product, ifc_propertyset_name, ifc_property_name):
    
    custom_property_list  = []
    
    if ifc_product:
        custom_property_list.append(ifcopenshell.util.element.get_pset(ifc_product, ifc_propertyset_name,ifc_property_name))
        
    if not custom_property_list:
        custom_property_list.append(None)
        
    return custom_property_list
    




class ConstructPandasDataFrame:

    def construct_dataframe(self):
        
        ifc_dictionary = defaultdict(list)
        
        for product in products:
            if product:
                ifc_dictionary['GlobalId'].append(str(product.GlobalId))
                ifc_dictionary['Name'].append(str(product.Name))
                ifc_dictionary['Type'].append(str(get_ifc_type(ifc_product=product)[0]))
                ifc_dictionary['IfcBuildingStorey'].append(get_ifc_building_storey(ifc_product=product)[0])
                ifc_dictionary['Classification'].append(get_ifc_classification_item_and_reference(ifc_product=product)[0])
            
        #print (ifc_dictionary)
        
        df = pd.DataFrame(ifc_dictionary)
        self.df = df
            
            
        print (df)

data_frame = ConstructPandasDataFrame()            
data_frame.construct_dataframe()     
        
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
