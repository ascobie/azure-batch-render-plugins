import bpy
import logging
import webbrowser

from batched_blender.constants import Constants

class MonitorPoolsOperator(bpy.types.Operator):
    bl_idname = Constants.OP_ID_MONITOR_POOLS
    bl_label = "MonitorPoolsOperator"

    def __init__(self):
        self.log = logging.getLogger(Constants.LOG_NAME)

    def execute(self, context):
        self.log.debug("MonitorPoolsOperator.execute")
        webbrowser.open(str.format("{}/{}", Constants.BATCH_LABS_BASE_URL, "pools"), 1, True)

        return {"FINISHED"}
