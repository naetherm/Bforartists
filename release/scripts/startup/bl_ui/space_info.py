# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>
import bpy
from bpy.types import Header, Menu


class INFO_HT_header(Header):
    bl_space_type = 'INFO'

    def draw(self, context):
        layout = self.layout
        layout.template_header()

        ALL_MT_editormenu.draw_hidden(_context, layout) # bfa - show hide the editormenu
        INFO_MT_editor_menus.draw_collapsible(context, layout)

class INFO_MT_editor_menus(Menu):
    bl_idname = "INFO_MT_editor_menus"
    bl_label = ""

    def draw(self, context):
        layout = self.layout
        layout.menu("INFO_MT_view")
        layout.menu("INFO_MT_info")


class INFO_MT_view(Menu):
    bl_label = "View"

    def draw(self, context):
        layout = self.layout

        layout.menu("INFO_MT_area")


class INFO_MT_info(Menu):
    bl_label = "Info"

    def draw(self, context):
        layout = self.layout

        layout.operator("info.select_all", text="Select All").action = 'SELECT'
        layout.operator("info.select_all", text="Deselect All").action = 'DESELECT'
        layout.operator("info.select_all", text="Invert Selection").action = 'INVERT'
        layout.operator("info.select_all", text="Toggle Selection").action = 'TOGGLE'

        layout.separator()

        layout.operator("info.select_box")

        layout.separator()

        # Disabled because users will likely try this and find
        # it doesn't work all that well in practice.
        # Mainly because operators needs to run in the right context.

        # layout.operator("info.report_replay")
        # layout.separator()

        layout.operator("info.report_delete", text="Delete")
        layout.operator("info.report_copy", text="Copy")


# bfa - show hide the editormenu
class ALL_MT_editormenu(Menu):
    bl_label = ""

    def draw(self, context):
        self.draw_menus(self.layout, context)

    @staticmethod
    def draw_menus(layout, context):

        row = layout.row(align=True)
        row.template_header() # editor type menus

# Workaround to separate the tooltips for Toggle Maximize Area
class INFO_OT_Toggle_Maximize_Area(bpy.types.Operator):
    """Toggle display selected area as maximized"""      # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "screen.toggle_maximized_area"        # unique identifier for buttons and menu items to reference.
    bl_label = "Toggle Maximize Area"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    def execute(self, context):        # execute() is called by blender when running the operator.
        bpy.ops.screen.screen_full_area(use_hide_panels = False)
        return {'FINISHED'}  


# Not really info, just add to re-usable location.
class INFO_MT_area(Menu):
    bl_label = "Area"

    def draw(self, context):
        layout = self.layout

        if context.space_data.type == 'VIEW_3D':
            layout.operator("screen.region_quadview", icon = "QUADVIEW")
            layout.separator()

        layout.operator("screen.area_split", text="Horizontal Split", icon = "SPLIT_HORIZONTAL").direction = 'HORIZONTAL'
        layout.operator("screen.area_split", text="Vertical Split", icon = "SPLIT_VERTICAL").direction = 'VERTICAL'

        layout.separator()

        layout.operator("screen.area_dupli", icon = "NEW_WINDOW")

        layout.separator()

        layout.operator("screen.toggle_maximized_area", text="Toggle Maximize Area", icon = "MAXIMIZE_AREA") # bfa - the separated tooltip.
        layout.operator("screen.screen_full_area", text="Toggle Fullscreen Area", icon='FULLSCREEN_ENTER').use_hide_panels = True


class INFO_MT_context_menu(Menu):
    bl_label = "Info Context Menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("info.report_copy", text="Copy")
        layout.operator("info.report_delete", text="Delete")


classes = (
    ALL_MT_editormenu,
    INFO_HT_header,
    INFO_OT_Toggle_Maximize_Area,
    INFO_MT_editor_menus,
    INFO_MT_area,
    INFO_MT_view,
    INFO_MT_info,
    INFO_MT_context_menu,
)

if __name__ == "__main__":  # only for live edit.
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
