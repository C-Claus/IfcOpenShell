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
import json
import bmesh
import logging
import numpy as np
from mathutils import Matrix
from math import radians
from blenderbim.bim.ifc import IfcStore


class ExportClashSets(bpy.types.Operator):
    bl_idname = "bim.export_clash_sets"
    bl_label = "Export Clash Sets"
    filename_ext = ".json"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def invoke(self, context, event):
        self.filepath = bpy.path.ensure_ext(bpy.data.filepath, ".json")
        WindowManager = context.window_manager
        WindowManager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        self.filepath = bpy.path.ensure_ext(self.filepath, ".json")
        clash_sets = []
        for clash_set in context.scene.BIMClashProperties.clash_sets:
            self.a = []
            self.b = []
            for ab in ["a", "b"]:
                for data in getattr(clash_set, ab):
                    clash_source = {"file": data.name}
                    if data.selector:
                        clash_source["selector"] = data.selector
                        clash_source["mode"] = data.mode
                    getattr(self, ab).append(clash_source)
            clash_sets.append({"name": clash_set.name, "tolerance": clash_set.tolerance, "a": self.a, "b": self.b})
        with open(self.filepath, "w") as destination:
            destination.write(json.dumps(clash_sets, indent=4))
        return {"FINISHED"}


class ImportClashSets(bpy.types.Operator):
    bl_idname = "bim.import_clash_sets"
    bl_label = "Import Clash Sets"
    bl_options = {"REGISTER", "UNDO"}
    filename_ext = ".json"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def invoke(self, context, event):
        self.filepath = bpy.path.ensure_ext(bpy.data.filepath, ".json")
        WindowManager = context.window_manager
        WindowManager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        with open(self.filepath) as f:
            clash_sets = json.load(f)
        for clash_set in clash_sets:
            new = context.scene.BIMClashProperties.clash_sets.add()
            new.name = clash_set["name"]
            new.tolerance = clash_set["tolerance"]
            for clash_source in clash_set["a"]:
                new_source = new.a.add()
                new_source.name = clash_source["file"]
                if "selector" in clash_source:
                    new_source.selector = clash_source["selector"]
                    new_source.mode = clash_source["mode"]
            if clash_set["b"]:
                for clash_source in clash_set["b"]:
                    new_source = new.b.add()
                    new_source.name = clash_source["file"]
                    if "selector" in clash_source:
                        new_source.selector = clash_source["selector"]
                        new_source.mode = clash_source["mode"]
        return {"FINISHED"}


class AddClashSet(bpy.types.Operator):
    bl_idname = "bim.add_clash_set"
    bl_label = "Add Clash Set"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        new = context.scene.BIMClashProperties.clash_sets.add()
        new.name = "New Clash Set"
        new.tolerance = 0.01
        return {"FINISHED"}


class RemoveClashSet(bpy.types.Operator):
    bl_idname = "bim.remove_clash_set"
    bl_label = "Remove Clash Set"
    bl_options = {"REGISTER", "UNDO"}
    index: bpy.props.IntProperty()

    def execute(self, context):
        context.scene.BIMClashProperties.clash_sets.remove(self.index)
        return {"FINISHED"}


class AddClashSource(bpy.types.Operator):
    bl_idname = "bim.add_clash_source"
    bl_label = "Add Clash Source"
    bl_options = {"REGISTER", "UNDO"}
    group: bpy.props.StringProperty()

    def execute(self, context):
        clash_set = context.scene.BIMClashProperties.active_clash_set
        source = getattr(clash_set, self.group).add()
        return {"FINISHED"}


class RemoveClashSource(bpy.types.Operator):
    bl_idname = "bim.remove_clash_source"
    bl_label = "Remove Clash Source"
    bl_options = {"REGISTER", "UNDO"}
    index: bpy.props.IntProperty()
    group: bpy.props.StringProperty()

    def execute(self, context):
        clash_set = context.scene.BIMClashProperties.active_clash_set
        getattr(clash_set, self.group).remove(self.index)
        return {"FINISHED"}


class SelectClashSource(bpy.types.Operator):
    bl_idname = "bim.select_clash_source"
    bl_label = "Select Clash Source"
    bl_options = {"REGISTER", "UNDO"}
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filter_glob: bpy.props.StringProperty(default="*.ifc", options={"HIDDEN"})
    index: bpy.props.IntProperty()
    group: bpy.props.StringProperty()

    def execute(self, context):
        clash_set = context.scene.BIMClashProperties.active_clash_set
        getattr(clash_set, self.group)[self.index].name = self.filepath
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


class SelectClashResults(bpy.types.Operator):
    bl_idname = "bim.select_clash_results"
    bl_label = "Select Clash Results"
    bl_options = {"REGISTER", "UNDO"}
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        context.scene.BIMClashProperties.clash_results_path = self.filepath
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


class SelectSmartGroupedClashesPath(bpy.types.Operator):
    bl_idname = "bim.select_smart_grouped_clashes_path"
    bl_label = "Select Smart-Grouped Clashes Path"
    bl_options = {"REGISTER", "UNDO"}
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        context.scene.BIMClashProperties.smart_grouped_clashes_path = self.filepath
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


class ExecuteIfcClash(bpy.types.Operator):
    bl_idname = "bim.execute_ifc_clash"
    bl_label = "Execute IFC Clash"
    filename_ext = ".bcf"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def invoke(self, context, event):
        if ".json" not in bpy.data.filepath:
            self.filepath = bpy.path.ensure_ext(bpy.data.filepath, ".bcf")
        WindowManager = context.window_manager
        WindowManager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        from ifcclash import ifcclash

        settings = ifcclash.ClashSettings()
        if ".json" not in self.filepath:
            self.filepath = bpy.path.ensure_ext(self.filepath, ".bcf")
        settings.output = self.filepath
        settings.logger = logging.getLogger("Clash")
        settings.logger.setLevel(logging.DEBUG)
        clasher = ifcclash.Clasher(settings)

        if context.scene.BIMClashProperties.should_create_clash_snapshots:

            def get_viewpoint_snapshot(viewpoint, mat):
                camera = bpy.data.objects.get("IFC Clash Camera")
                if not camera:
                    camera = bpy.data.objects.new("IFC Clash Camera", bpy.data.cameras.new("IFC Clash Camera"))
                    context.scene.collection.objects.link(camera)
                camera.matrix_world = Matrix(mat)
                context.scene.camera = camera
                camera.data.angle = radians(60)
                area = next(area for area in context.screen.areas if area.type == "VIEW_3D")
                area.spaces[0].region_3d.view_perspective = "CAMERA"
                area.spaces[0].shading.show_xray = True
                context.scene.render.resolution_x = 480
                context.scene.render.resolution_y = 270
                context.scene.render.image_settings.file_format = "PNG"
                context.scene.render.filepath = os.path.join(context.scene.BIMProperties.data_dir, "snapshot.png")
                bpy.ops.render.opengl(write_still=True)
                return context.scene.render.filepath

            clasher.get_viewpoint_snapshot = get_viewpoint_snapshot

        clasher.clash_sets = []
        for clash_set in context.scene.BIMClashProperties.clash_sets:
            self.a = []
            self.b = []
            for ab in ["a", "b"]:
                for data in getattr(clash_set, ab):
                    clash_source = {"file": data.name}
                    if data.selector:
                        clash_source["selector"] = data.selector
                        clash_source["mode"] = data.mode
                    getattr(self, ab).append(clash_source)
            clash_set_data = {"name": clash_set.name, "tolerance": clash_set.tolerance, "a": self.a}
            if self.b:
                clash_set_data["b"] = self.b
            clasher.clash_sets.append(clash_set_data)
        clasher.clash()
        clasher.export()
        return {"FINISHED"}


class SelectIfcClashResults(bpy.types.Operator):
    bl_idname = "bim.select_ifc_clash_results"
    bl_label = "Select IFC Clash Results"
    bl_options = {"REGISTER", "UNDO"}
    filename_ext = ".json"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def invoke(self, context, event):
        self.filepath = bpy.path.ensure_ext(bpy.data.filepath, ".json")
        WindowManager = context.window_manager
        WindowManager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        self.filepath = bpy.path.ensure_ext(self.filepath, ".json")
        with open(self.filepath) as f:
            clash_sets = json.load(f)
        clash_set_name = context.scene.BIMClashProperties.active_clash_set.name
        global_ids = []
        for clash_set in clash_sets:
            if clash_set["name"] != clash_set_name:
                continue
            if not "clashes" in clash_set.keys():
                self.report({"WARNING"}, "No clashes found for the selected Clash Set.")
                return {"CANCELLED"}
            for clash in clash_set["clashes"].values():
                global_ids.extend([clash["a_global_id"], clash["b_global_id"]])
        for obj in context.visible_objects:
            if not obj.BIMObjectProperties.ifc_definition_id:
                continue
            element = self.file.by_id(obj.BIMObjectProperties.ifc_definition_id)
            if element.GlobalId in global_ids:
                obj.select_set(True)
        return {"FINISHED"}


class SmartClashGroup(bpy.types.Operator):
    bl_idname = "bim.smart_clash_group"
    bl_label = "Smart Group Clashes"
    bl_options = {"REGISTER", "UNDO"}
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    @classmethod
    def poll(cls, context):
        return context.scene.BIMClashProperties.clash_results_path

    def execute(self, context):
        import ifcclash

        settings = ifcclash.IfcClashSettings()
        self.filepath = bpy.path.ensure_ext(context.scene.BIMClashProperties.clash_results_path, ".json")
        settings.output = self.filepath
        settings.logger = logging.getLogger("Clash")
        settings.logger.setLevel(logging.DEBUG)
        ifc_clasher = ifcclash.IfcClasher(settings)

        with open(self.filepath) as f:
            clash_sets = json.load(f)

        # execute the smart grouping
        save_path = bpy.path.ensure_ext(context.scene.BIMClashProperties.smart_grouped_clashes_path, ".json")
        smart_grouped_clashes = ifc_clasher.smart_group_clashes(
            clash_sets, context.scene.BIMClashProperties.smart_clash_grouping_max_distance
        )

        # save smart_groups to json
        with open(save_path, "w") as f:
            f.write(json.dumps(smart_grouped_clashes))

        clash_set_name = context.scene.BIMClashProperties.active_clash_set.name

        # Reset the list of smart_clash_groups for the UI
        context.scene.BIMClashProperties.smart_clash_groups.clear()

        for clash_set, smart_groups in smart_grouped_clashes.items():
            # Only select the clashes that correspond to the actively selected IFC Clash Set
            if clash_set != clash_set_name:
                continue
            else:
                for smart_group, global_id_pairs in smart_groups[0].items():
                    new_group = context.scene.BIMClashProperties.smart_clash_groups.add()
                    new_group.number = f"{smart_group}"

                    for pair in global_id_pairs:
                        for id in pair:
                            new_global_id = new_group.global_ids.add()
                            new_global_id.name = id

        return {"FINISHED"}


class LoadSmartGroupsForActiveClashSet(bpy.types.Operator):
    bl_idname = "bim.load_smart_groups_for_active_clash_set"
    bl_label = "Load Smart Groups for Active Clash Set"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.scene.BIMClashProperties.active_clash_set

    def execute(self, context):
        smart_groups_path = bpy.path.ensure_ext(context.scene.BIMClashProperties.smart_grouped_clashes_path, ".json")

        clash_set_name = context.scene.BIMClashProperties.active_clash_set.name

        with open(smart_groups_path) as f:
            smart_grouped_clashes = json.load(f)

        # Reset the list of smart_clash_groups for the UI
        context.scene.BIMClashProperties.smart_clash_groups.clear()

        for clash_set, smart_groups in smart_grouped_clashes.items():
            # Only select the clashes that correspond to the actively selected IFC Clash Set
            if clash_set != clash_set_name:
                continue
            else:
                for smart_group, global_id_pairs in smart_groups[0].items():
                    new_group = context.scene.BIMClashProperties.smart_clash_groups.add()
                    new_group.number = f"{smart_group}"
                    for pair in global_id_pairs:
                        for id in pair:
                            new_global_id = new_group.global_ids.add()
                            new_global_id.name = id

        return {"FINISHED"}


class SelectSmartGroup(bpy.types.Operator):
    bl_idname = "bim.select_smart_group"
    bl_label = "Select Smart Group"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return IfcStore.get_file() and context.visible_objects and context.scene.BIMClashProperties.active_smart_group

    def execute(self, context):
        self.file = IfcStore.get_file()
        # Select smart group in view
        selected_smart_group = context.scene.BIMClashProperties.active_smart_group
        # print(selected_smart_group.number)

        for obj in context.visible_objects:
            if not obj.BIMObjectProperties.ifc_definition_id:
                continue
            element = self.file.by_id(obj.BIMObjectProperties.ifc_definition_id)
            for id in selected_smart_group.global_ids:
                # print("Id: ", id)
                # print("Global id: ", element.GlobalId)
                if element.GlobalId in id.name:
                    # print("object match: ", global_id)
                    obj.select_set(True)

        return {"FINISHED"}


class BlenderClasher:
    def process_clash_set(self, context):
        import collision

        a_cm = collision.CollisionManager()
        b_cm = collision.CollisionManager()
        self.add_to_cm(a_cm, context.scene.BIMClashProperties.blender_clash_set_a, context)
        self.add_to_cm(b_cm, context.scene.BIMClashProperties.blender_clash_set_b, context)
        results = a_cm.in_collision_other(b_cm, return_data=True)
        if not results[0]:
            print("No clashes")
            return
        for contact in results[1]:
            if contact.raw.penetration_depth < 0.01:
                continue
            print("-----")
            print(contact.names)
            print(contact.raw.normal)
            print(contact.raw.pos)

    def add_to_cm(self, cm, object_names, context):
        import ifcclash

        for object_name in object_names:
            name = object_name.name
            obj = bpy.data.objects[name]
            triangulated_mesh = self.triangulate_mesh(obj, context)
            mesh = ifcclash.Mesh()
            mesh.vertices = np.array([tuple(obj.matrix_world @ v.co) for v in triangulated_mesh.vertices])
            mesh.faces = np.array([tuple(p.vertices) for p in triangulated_mesh.polygons])
            cm.add_object(name, mesh)

    def triangulate_mesh(self, obj, context):
        mesh = obj.evaluated_get(context.evaluated_depsgraph_get()).to_mesh()
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bmesh.ops.triangulate(bm, faces=bm.faces)
        bm.to_mesh(mesh)
        bm.free()
        del bm
        return mesh


class SetBlenderClashSetA(bpy.types.Operator):
    bl_idname = "bim.set_blender_clash_set_a"
    bl_label = "Set Blender Clash Set A"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        context.scene.BIMClashProperties.blender_clash_set_a.clear()
        for obj in context.selected_objects:
            new = context.scene.BIMClashProperties.blender_clash_set_a.add()
            new.name = obj.name
        return {"FINISHED"}


class SetBlenderClashSetB(bpy.types.Operator):
    bl_idname = "bim.set_blender_clash_set_b"
    bl_label = "Set Blender Clash Set B"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        context.scene.BIMClashProperties.blender_clash_set_b.clear()
        for obj in context.selected_objects:
            new = context.scene.BIMClashProperties.blender_clash_set_b.add()
            new.name = obj.name
        return {"FINISHED"}


class ExecuteBlenderClash(bpy.types.Operator):
    bl_idname = "bim.execute_blender_clash"
    bl_label = "Execute Blender Clash"

    def execute(self, context):
        blender_clasher = BlenderClasher()
        blender_clasher.process_clash_set(context)
        return {"FINISHED"}
