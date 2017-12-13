import bpy
import logging
import webbrowser
import os

from batched_blender.ui import ui_shared
from batched_blender.utils import BatchOps

class BatchSettings(object):
    """
    Initializes and manages the Batch Apps addon session.
    Registers all classes and handles all sub-pages.
    Defines the display of the global HOME and ERROR pages.
    Also configures logging and User Preferences.
    """

    pages = ["HOME", "ERROR"]

    def __init__(self):
        self.ops = self._register_ops()
        self.ui = self._register_ui()
        self.props = self._register_props()
        self.log = self._configure_logging()
        self.start()

    def _configure_logging(self):
        """
        Configures the logger for the addon based on the User Preferences.
        Sets up a stream handler to log to Blenders console and a file
        handler to log to the Batch log file.
        """
        logger = logging.getLogger('batched_blender')
        logger.setLevel(int(self.props.log_level))
        console_format = logging.Formatter("Batch: [%(levelname)s] %(message)s")
        file_format = logging.Formatter("%(asctime)-15s [%(levelname)s] %(module)s: %(message)s")

        console_logging = logging.StreamHandler()
        console_logging.setFormatter(console_format)
        logger.addHandler(console_logging)
        logfile = os.path.join(self.props.log_dir, "batched_blender.log")
        file_logging = logging.FileHandler(logfile)
        file_logging.setFormatter(file_format)
        logger.addHandler(file_logging)

        return logger


    def _register_ops(self):
        """
        Registers the shared operators with a batch_shared prefix.

        :Returns:
            - A list of the names (str) of the registered operators.
        """
        ops = []
        ops.append(BatchOps.register("shared.submit_job", "Submit Job", self._submit_job))
        ops.append(BatchOps.register("shared.monitor_jobs", "Monitor Jobs", self._monitor_jobs))
        ops.append(BatchOps.register("shared.monitor_pools", "Monitor Pools", self._monitor_pools))
        ops.append(BatchOps.register("shared.download_renders", "Download Renders", self._download_renders))
        ops.append(BatchOps.register("shared.home", "Home", self._home))

        return ops


    def _register_props(self):
        """
        Retrieves the shared addon properties - in this case the User
        Preferences.

        :Returns:
            - :class:`.UserPreferences`
        """
        props = bpy.context.user_preferences.addons[__package__].preferences
        if not os.path.isdir(props.log_dir):
            try:
                os.mkdir(props.log_dir)
            except:
                raise EnvironmentError(
                    "Data directory not created at '{0}'.\n"
                    "Please ensure you have adequate permissions.".format(props.log_dir))
        return props


    def _register_ui(self):
        """
        Matches the HOME and ERROR pages with their corresponding
        ui functions.

        :Returns:
            - A dictionary mapping the page name to its corresponding
              ui function.
        """
        def get_shared_ui(name):
            name = name.lower()
            return getattr(ui_shared, name)

        page_func = map(get_shared_ui, self.pages)
        return dict(zip(self.pages, page_func))


    def _home(self, op, context):
        """
        The execute method for the shared.home operator.
        Sets the session page to HOME.

        :Args:
            - op (:class:`bpy.types.Operator`): An instance of the current
              operator class.
            - context (:class:`bpy.types.Context`): The current blender
              context.

        :Returns:
            - Blender-specific value {'FINISHED'} to indicate the operator has
              completed its action.
        """
        self.page = "HOME"
        return {'FINISHED'}


    def _submit_job(self, op, context):
        """
        The execute method for the shared._submit_job operator.

        :Args:
            - op (:class:`bpy.types.Operator`): An instance of the current
              operator class.
            - context (:class:`bpy.types.Context`): The current blender
              context.

        :Returns:
            - Blender-specific value {'FINISHED'} to indicate the operator has
              completed its action.
        """

        bpy.context.scene.batch_session.log.debug("Submit job ... " + bpy.data.filepath)
        bpy.context.scene.batch_session.log.debug(bpy.context.scene)
        # webbrowser.open("https://ms.portal.azure.com/", 2, True)
        
        return {'FINISHED'}


    def _monitor_jobs(self, op, context):
        """
        The execute method for the shared._monitor_jobs operator.

        :Args:
            - op (:class:`bpy.types.Operator`): An instance of the current
              operator class.
            - context (:class:`bpy.types.Context`): The current blender
              context.

        :Returns:
            - Blender-specific value {'FINISHED'} to indicate the operator has
              completed its action.
        """

        bpy.context.scene.batch_session.log.debug("Monitor jobs ... ")
        # webbrowser.open("https://ms.portal.azure.com/", 2, True)
        
        return {'FINISHED'}


    def _monitor_pools(self, op, context):
        """
        The execute method for the shared._monitor_pools operator.

        :Args:
            - op (:class:`bpy.types.Operator`): An instance of the current
              operator class.
            - context (:class:`bpy.types.Context`): The current blender
              context.

        :Returns:
            - Blender-specific value {'FINISHED'} to indicate the operator has
              completed its action.
        """

        bpy.context.scene.batch_session.log.debug("Monitor pools ... ")
        # webbrowser.open("https://ms.portal.azure.com/", 2, True)
        
        return {'FINISHED'}

    
    def _download_renders(self, op, context):
        """
        The execute method for the shared._download_renders operator.

        :Args:
            - op (:class:`bpy.types.Operator`): An instance of the current
              operator class.
            - context (:class:`bpy.types.Context`): The current blender
              context.

        :Returns:
            - Blender-specific value {'FINISHED'} to indicate the operator has
              completed its action.
        """

        bpy.context.scene.batch_session.log.debug("Download renders ... ")
        # webbrowser.open("https://ms.portal.azure.com/", 2, True)
        
        return {'FINISHED'}


    def display(self, ui, layout):
        """
        Invokes the corresponding ui function depending on the session's
        current page.

        :Args:
            - ui (blender :class:`.Interface`): The instance of the Interface
              panel class.
            - layout (blender :class:`bpy.types.UILayout`): The layout object,
              derived from the Interface panel. Used for creating ui
              components.

        :Returns:
            - Runs the display function for the applicable page.
        """
        return self.ui[self.page](ui, layout)


    def start(self):
        """
        Initialize all the addon subpages
        Sets page to HOME.
        """

        self.log.debug("Initialised home module")
        self.page = "HOME"
        

    def redraw(self):
        """
        Somewhat hacky way to force Blender to redraw the UI.
        """
        bpy.context.scene.objects.active = bpy.context.scene.objects.active

