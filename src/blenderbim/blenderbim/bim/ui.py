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

import os
import bpy
from . import ifc
from bpy.types import Panel
from bpy.props import StringProperty, IntProperty, BoolProperty


class BIM_PT_section_plane(Panel):
    bl_label = "Temporary Section Cutaways"
    bl_idname = "BIM_PT_section_plane"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "output"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        props = context.scene.BIMProperties

        row = layout.row()
        row.prop(props, "should_section_selected_objects")

        row = layout.row()
        row.prop(props, "section_plane_colour")

        row = layout.row(align=True)
        row.operator("bim.add_section_plane")
        row.operator("bim.remove_section_plane")


class BIM_UL_generic(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if item:
            layout.prop(item, "name", text="", emboss=False)
        else:
            layout.label(text="", translate=False)


class BIM_UL_topics(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        ob = data
        if item:
            layout.prop(item, "title", text="", emboss=False)
        else:
            layout.label(text="", translate=False)


class BIM_ADDON_preferences(bpy.types.AddonPreferences):
    bl_idname = "blenderbim"
    svg2pdf_command: StringProperty(name="SVG to PDF Command", description="E.g. [['inkscape', svg, '-o', pdf]]")
    svg2dxf_command: StringProperty(
        name="SVG to DXF Command",
        description="E.g. [['inkscape', svg, '-o', eps], ['pstoedit', '-dt', '-f', 'dxf:-polyaslines -mm', eps, dxf, '-psarg', '-dNOSAFER']]",
    )
    svg_command: StringProperty(name="SVG Command", description="E.g. [['firefox-bin', path]]")
    pdf_command: StringProperty(name="PDF Command", description="E.g. [['firefox-bin', path]]")
    openlca_port: IntProperty(name="OpenLCA IPC Port", default=8080)
    should_hide_empty_props: BoolProperty(name="Should Hide Empty Properties", default=True)
    should_play_chaching_sound: BoolProperty(
        name="Should Make A Cha-Ching Sound When Project Costs Updates", default=False
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(
            text="To upgrade, first uninstall your current BlenderBIM Add-on, then install the new version.",
            icon="ERROR",
        )
        row = layout.row()
        row.label(
            text="To uninstall, first disable the add-on. Then restart Blender before pressing the 'Remove' button.",
            icon="ERROR",
        )
        row = layout.row()
        row.operator("bim.open_upstream", text="Visit Homepage").page = "home"
        row.operator("bim.open_upstream", text="Visit Documentation").page = "docs"
        row = layout.row()
        row.operator("bim.open_upstream", text="Visit Wiki").page = "wiki"
        row.operator("bim.open_upstream", text="Visit Community").page = "community"
        row = layout.row()
        row.prop(self, "svg2pdf_command")
        row = layout.row()
        row.prop(self, "svg2dxf_command")
        row = layout.row()
        row.prop(self, "svg_command")
        row = layout.row()
        row.prop(self, "pdf_command")
        row = layout.row()
        row.prop(self, "openlca_port")
        row = layout.row()
        row.prop(self, "should_hide_empty_props")
        row = layout.row()
        row.prop(self, "should_play_chaching_sound")


def ifc_units(self, context):
    scene = context.scene
    props = scene.BIMProperties
    layout = self.layout
    layout.use_property_decorate = False
    layout.use_property_split = True
    row = layout.row()
    row.prop(props, "area_unit")
    row = layout.row()
    row.prop(props, "volume_unit")
    row = layout.row()
    if scene.unit_settings.system == "IMPERIAL":
        row.prop(props, "imperial_precision")
    else:
        row.prop(props, "metric_precision")
