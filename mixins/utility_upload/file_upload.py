
from collections import OrderedDict
import decimal
import pandas
from django.db import connection
import os
import imghdr
import base64
import time 
from django.conf import settings
from django.core.files.storage import FileSystemStorage










def document_upload(datafile, file_name, file_folder):
    """
        Upload file
        Args:
            datafile (str): uploaded file object
            file_name (str): uplaod file name
            file_folder (str): destination folder
        Returns:
            str: Uploaded file path
    """

    file_name = file_name.replace(' ', '_')
    user_path_filename = os.path.join(settings.MEDIA_ROOT, file_folder)
    if not os.path.exists(user_path_filename):
        os.makedirs(user_path_filename)
    fs = FileSystemStorage(location=user_path_filename)

    myfile_name = str(int(round(time.time() * 1000))) + "_" + str(datafile.name) #+ str(file_name) + "_" 
    filename = fs.save(myfile_name, datafile)
    full_file_path = myfile_name   #"media/" + file_folder + "/" + myfile_name

    return full_file_path

