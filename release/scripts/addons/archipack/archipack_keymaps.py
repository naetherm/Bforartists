# -*- coding:utf-8 -*-

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
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110- 1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

# ----------------------------------------------------------
# Author: Stephen Leger (s-leger)
#
# ----------------------------------------------------------


class Keymaps:
    """
        Expose user defined keymaps as event
        so in modal operator we are able to
        identify like
        if (event == keymap.undo.event):

        and in feedback panels:
            keymap.undo.key
            keymap.undo.name
    """
    def __init__(self, context):
        """
            Init keymaps properties
        """

        # undo event
        self.undo = self.get_event(context, 'Screen', 'ed.undo')

        # delete event
        self.delete = self.get_event(context, 'Object Mode', 'object.delete')

        """
        # provide abstration between user and addon
        # with different select mouse side
        mouse_right = context.window_manager.keyconfigs.active.preferences.select_mouse
        if mouse_right == 'LEFT':
            mouse_left = 'RIGHT'
            mouse_right_side = 'Left'
            mouse_left_side = 'Right'
        else:
            mouse_left = 'LEFT'
            mouse_right_side = 'Right'
            mouse_left_side = 'Left'

        self.leftmouse = mouse_left + 'MOUSE'
        self.rightmouse = mouse_right + 'MOUSE'
        """

    def check(self, event, against):
        res = False
        signature = (event.alt, event.ctrl, event.shift, event.type, event.value)
        for ev in against:
            # print ("check %s == %s" % (signature, ev))
            if ev['event'] == signature:
                # print("check True")
                res = True
                break
        return res

    def get_event(self, context, keyconfig, keymap_item):
        """
            Return simple keymaps event signature as array of dict
            NOTE:
                this won't work for complex keymaps such as select_all
                using properties to call operator in different manner
            type: keyboard main type
            name: event name as defined in user preferences
            event: simple event signature to compare  like :
              if keymap.check(event, keymap.undo):
        """
        evs = [ev for k, ev in context.window_manager.keyconfigs[0].keymaps[keyconfig].keymap_items.items()
               if k == keymap_item]
        # ev = context.window_manager.keyconfigs[0].keymaps[keyconfig].keymap_items[keymap_item]
        res = []
        for ev in evs:
            key = ev.type
            if ev.ctrl:
                key += '+CTRL'
            if ev.alt:
                key += '+ALT'
            if ev.shift:
                key += '+SHIFT'
            res.append({'type': key, 'name': ev.name, 'event': (ev.alt, ev.ctrl, ev.shift, ev.type, ev.value)})
        return res

    def dump_keys(self, context, filename="/tmp/keymap.txt"):
        """
            Utility for developpers :
            Dump all keymaps to a file
            filename : string a file path to dump keymaps
        """
        str = ""
        kms = context.window_manager.keyconfigs
        for name, km in kms.items():
            for key in km.keymaps.keys():
                str += "\n\n#--------------------------------\n{} - {}:\n#--------------------------------\n\n".format(name, key)
                for sub in km[key].keymap_items.keys():
                    k = km[key].keymap_items[sub]
                    str += "alt:{} ctrl:{} shift:{} type:{} value:{}  idname:{} name:{}\n".format(
                        k.alt, k.ctrl, k.shift, k.type, k.value, sub, k.name)
        file = open(filename, "w")
        file.write(str)
        file.close()