import bpy
import logging
import webbrowser

class MonitorJobsOperator(bpy.types.Operator):
    bl_idname = "batch_shared.monitor_jobs"
    bl_label = "MonitorJobsOperator"

    def __init__(self):
        self.log = logging.getLogger('batched_blender')

    def execute(self, context):
        self.log.debug("MonitorJobsOperator.execute")
        # webbrowser.open("ms-batchlabs://route/jobs", 1, True)

        return {"FINISHED"}
