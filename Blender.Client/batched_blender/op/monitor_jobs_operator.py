import bpy
import logging
import webbrowser

from batched_blender.constants import Constants

class MonitorJobsOperator(bpy.types.Operator):
    bl_idname = Constants.OP_ID_MONITOR_JOBS
    bl_label = "MonitorJobsOperator"

    def __init__(self):
        self.log = logging.getLogger(Constants.LOG_NAME)

    def execute(self, context):
        self.log.debug("MonitorJobsOperator.execute")
        webbrowser.open(str.format("{}/{}", Constants.BATCH_LABS_BASE_URL, "jobs"), 1, True)

        return {"FINISHED"}
