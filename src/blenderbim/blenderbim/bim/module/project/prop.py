# BlenderBIM Add-on - OpenBIM Blender Add-on
# Copyright (C) 2020, 2021 Dion Moult <dion@thinkmoult.com>
#
# This file is part of BlenderBIM Add-on.
#
# BlenderBIM Add-on is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BlenderBIM Add-on is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BlenderBIM Add-on.  If not, see <http://www.gnu.org/licenses/>.

import bpy
from blenderbim.bim.ifc import IfcStore
from blenderbim.bim.prop import StrProperty
from bpy.types import PropertyGroup
from bpy.props import (
    StringProperty,
    BoolProperty,
    FloatProperty,
    IntProperty,
    CollectionProperty,
)


def update_filter_mode(self, context):
    self.filter_categories.clear()
    if self.filter_mode == "NONE":
        return
    file = IfcStore.get_file()
    if self.filter_mode == "DECOMPOSITION":
        if file.schema == "IFC2X3":
            elements = file.by_type("IfcSpatialStructureElement")
        else:
            elements = file.by_type("IfcSpatialElement")
        for element in elements:
            new = self.filter_categories.add()
            new.name = "{}/{}".format(element.is_a(), element.Name or "Unnamed")
            new.ifc_definition_id = element.id()
            new.total_elements = sum([len(r.RelatedElements) for r in element.ContainsElements])
    elif self.filter_mode == "IFC_CLASS":
        for ifc_class in sorted(list(set([e.is_a() for e in file.by_type("IfcElement")]))):
            new = self.filter_categories.add()
            new.name = ifc_class
            new.total_elements = len(file.by_type(ifc_class, include_subtypes=False))


class LibraryElement(PropertyGroup):
    name: StringProperty(name="Name")
    ifc_definition_id: IntProperty(name="IFC Definition ID")
    is_declared: BoolProperty(name="Is Declared", default=False)
    is_appended: BoolProperty(name="Is Appended", default=False)


class FilterCategory(PropertyGroup):
    name: StringProperty(name="Name")
    ifc_definition_id: IntProperty(name="IFC Definition ID")
    is_selected: BoolProperty(name="Is Selected", default=False)
    total_elements: IntProperty(name="Total Elements")


class Link(PropertyGroup):
    name: StringProperty(name="Name")
    is_loaded: BoolProperty(name="Is Loaded", default=False)


class BIMProjectProperties(PropertyGroup):
    is_authoring: BoolProperty(name="Enable Authoring Mode", default=True)
    is_editing: BoolProperty(name="Is Editing", default=False)
    is_loading: BoolProperty(name="Is Loading", default=False)
    mvd: StringProperty(name="MVD")
    author_name: StringProperty(name="Author")
    author_email: StringProperty(name="Author Email")
    organisation_name: StringProperty(name="Organisation")
    organisation_email: StringProperty(name="Organisation Email")
    authorisation: StringProperty(name="Authoriser")
    active_library_element: StringProperty(name="Enable Authoring Mode", default="")
    library_breadcrumb: CollectionProperty(name="Library Breadcrumb", type=StrProperty)
    library_elements: CollectionProperty(name="Library Elements", type=LibraryElement)
    active_library_element_index: IntProperty(name="Active Library Element Index")
    collection_mode: bpy.props.EnumProperty(
        items=[
            ("DECOMPOSITION", "Decomposition", "Collections represent aggregates and spatial containers"),
            ("SPATIAL_DECOMPOSITION", "Spatial Decomposition", "Collections represent spatial containers"),
            ("IFC_CLASS", "IFC Class", "Collections represent IFC class"),
            ("NONE", "None", "No collections are created"),
        ],
        name="Collection Mode",
    )
    filter_mode: bpy.props.EnumProperty(
        items=[
            ("NONE", "None", "No filtering is performed"),
            ("DECOMPOSITION", "Decomposition", "Filter objects by decomposition"),
            ("IFC_CLASS", "IFC Class", "Filter objects by class"),
            ("WHITELIST", "Whitelist", "Filter objects using a custom whitelist query"),
            ("BLACKLIST", "Blacklist", "Filter objects using a custom blacklist query"),
        ],
        name="Filter Mode",
        update=update_filter_mode
    )
    filter_categories: CollectionProperty(name="Filter Categories", type=FilterCategory)
    active_filter_category_index: IntProperty(name="Active Filter Category Index")
    filter_query: StringProperty(name="Filter Query")
    should_use_cpu_multiprocessing: BoolProperty(name="Import with CPU Multiprocessing", default=True)
    should_merge_by_class: BoolProperty(name="Import and Merge by Class", default=False)
    should_merge_by_material: BoolProperty(name="Import and Merge by Material", default=False)
    should_merge_materials_by_colour: BoolProperty(name="Import and Merge Materials by Colour", default=False)
    should_clean_mesh: BoolProperty(name="Import and Clean Mesh", default=True)
    deflection_tolerance: FloatProperty(name="Import Deflection Tolerance", default=0.001)
    angular_tolerance: FloatProperty(name="Import Angular Tolerance", default=0.5)
    should_offset_model: BoolProperty(name="Import and Offset Model", default=False)
    model_offset_coordinates: StringProperty(name="Model Offset Coordinates", default="0,0,0")
    links: CollectionProperty(name="Links", type=Link)
    active_link_index: IntProperty(name="Active Link Index")


    def get_library_element_index(self, lib_element):
        return next((i for i in range(len(self.library_elements)) if self.library_elements[i] == lib_element))
