import bpy
import logging
import webbrowser

class MonitorPoolsOperator(bpy.types.Operator):
    bl_idname = "batch_shared.monitor_pools"
    bl_label = "MonitorPoolsOperator"

    def __init__(self):
        self.log = logging.getLogger("batched_blender")

    def execute(self, context):
        self.log.debug("MonitorPoolsOperator.execute")
        # webbrowser.open("ms-batchlabs://route/pools", 1, True)

        return {"FINISHED"}
