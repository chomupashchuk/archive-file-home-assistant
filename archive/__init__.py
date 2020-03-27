import os
import time
import logging
from zipfile import ZipFile
import homeassistant.util.dt as dt_utils

ATTR_FILE = "file"
ATTR_FOLDER = "folder"
ATTR_TIME = "time"
ATTR_ONLY = "only_extensions"
ATTR_EXCEPT = "except_extensions"
ATTR_TARGET = "target"
ATTR_NAME = "name"
SERVICE_FILE = "file"
SERVICE_FOLDER = "files_in_folder"
DEFAULT_FILE = ""
DEFAULT_FOLDER = ""
DEFAULT_TARGET = ""
DEFAULT_NAME = ""
DEFAULT_EXTENSION = []
DEFAULT_TIME = 3600
DOMAIN = "archive"

_LOGGER = logging.getLogger(__name__)

def setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""
    
    def handle_archive_file(call):
        """Handle the service call."""
        file_path = call.data.get(ATTR_FILE, DEFAULT_FILE)
        target_path = call.data.get(ATTR_TARGET, DEFAULT_TARGET)
        archive_name = call.data.get(ATTR_NAME, DEFAULT_NAME)
    
        if not os.path.isfile(file_path):
            _LOGGER.info("{} is not a file".format(file_path))
            raise
        
        if target_path != DEFAULT_TARGET:
            if not os.path.isdir(target_path):
                try:
                    os.mkdir(target_path)
                except:
                    _LOGGER.info("{} could not be created".format(target_path))
                    raise
        else:
            target_path = os.path.dirname(file_path)
        
        if archive_name == DEFAULT_NAME:
            archive_name = dt_utils.utcnow().strftime("%Y_%m_%d_%H_%M_%S") + '.zip'
        else:
            archive_name += '.zip'
            
        try:
            with ZipFile(os.path.join(target_path, archive_name), 'w') as zipObj:
                _LOGGER.info("Archived {}".format(file_path))
                zipObj.write(file_path)
        except:
            _LOGGER.info("{} could not be created".format(archive_name))
            raise

    def handle_archive_files_in_folder(call):
        """Handle the service call."""
        folder_path = call.data.get(ATTR_FOLDER, DEFAULT_FOLDER)
        folder_time = call.data.get(ATTR_TIME, DEFAULT_TIME)
        exceptions = call.data.get(ATTR_EXCEPT, DEFAULT_EXTENSION)
        specified = call.data.get(ATTR_ONLY, DEFAULT_EXTENSION)
        target_path = call.data.get(ATTR_TARGET, DEFAULT_TARGET)
        archive_name = call.data.get(ATTR_NAME, DEFAULT_NAME)
        now = time.time()
        
        if not os.path.isdir(folder_path):
            _LOGGER.info("{} is not a folder".format(folder_path))
            raise

        except_extensions = []
        if isinstance(exceptions, str):
            except_extensions.append(exceptions)
        elif isinstance(exceptions, list):
            except_extensions = exceptions
        
        only_extensions = []
        if isinstance(specified, str):
            only_extensions.append(specified)
        elif isinstance(specified, list):
            only_extensions = specified
        
        if only_extensions != [] and except_extensions != []:
            _LOGGER.info("Not allowed to mix extensions both only allowed and excluded")
            raise
        
        if target_path != DEFAULT_TARGET:
            if not os.path.isdir(target_path):
                try:
                    os.mkdir(target_path)
                except:
                    _LOGGER.info("{} could not be created".format(target_path))
                    raise
        else:
            target_path = folder_path
        
        if archive_name == DEFAULT_NAME:
            archive_name = dt_utils.utcnow().strftime("%Y_%m_%d_%H_%M_%S") + '.zip'
        else:
            archive_name += '.zip'
        
        try:
            with ZipFile(os.path.join(target_path, archive_name), 'w') as zipObj:
                for file in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file)
                    if os.stat(file_path).st_mtime < now - folder_time:
                        if os.path.isfile(file_path):
                            archive_file = True
                            if only_extensions != []:
                                archive_file = False
                                for extension in only_extensions:
                                    if file.endswith(extension):
                                        archive_file = True
                                        break
                            if except_extensions != []:
                                for extension in except_extensions:
                                    if file.endswith(extension):
                                        archive_file = False
                                        break
                            if archive_file and archive_name + '.zip' != file:
                                _LOGGER.info("Archived {}".format(file_path))
                                zipObj.write(file_path)
        except:
            _LOGGER.info("{} could not be created".format(archive_name))
            raise
        
    hass.services.register(DOMAIN, SERVICE_FILE, handle_archive_file)
    hass.services.register(DOMAIN, SERVICE_FOLDER, handle_archive_files_in_folder)
    # Return boolean to indicate that initialization was successfully.
    return True