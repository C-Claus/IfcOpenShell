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
from . import ui, prop, operator

classes = (
    operator.EnableEditingAttributes,
    operator.DisableEditingAttributes,
    operator.EditAttributes,
    operator.GenerateGlobalId,
    prop.BIMAttributeProperties,
    ui.BIM_PT_object_attributes,
    ui.BIM_PT_material_attributes,
)


def register():
    bpy.types.Object.BIMAttributeProperties = bpy.props.PointerProperty(type=prop.BIMAttributeProperties)
    bpy.types.Material.BIMAttributeProperties = bpy.props.PointerProperty(type=prop.BIMAttributeProperties)


def unregister():
    del bpy.types.Object.BIMAttributeProperties
    del bpy.types.Material.BIMAttributeProperties
