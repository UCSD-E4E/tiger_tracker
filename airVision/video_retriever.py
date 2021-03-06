import os

# Returns a list of all the airvision video 
# directories (2013/10/22/13, 2013/10/22/14...) 
# below the Videos directory
# Paramters: path to the Videos directory
# (For example:
# "/Programdata/airvision/data/camera/videos")
# Return: a list with the dates of the video
# directories (2013/10/22/13), a list with
# the camera ids, and a list with the 
# absolute paths to the video directories
def grab_video_dirs(path):
    video_dates = []
    camera_ids = []
    video_dirs_abs = []  
    
    for root, dirs, files in os.walk(path):
        rel_path = os.path.relpath(root,path)
        if rel_path.count("/") == 4:
            exclude1 = rel_path.startswith("temp") == False
            exclude2 = rel_path.endswith("meta") == False       
            if exclude1 and exclude2:
                video_dirs_abs.append(root)
                id_and_date = rel_path.partition("/")        
                video_dates.append(id_and_date[2])
                camera_ids.append(id_and_date[0])
    
    return video_dates, camera_ids, video_dirs_abs


# Break up absolute path of an airvision video to the
# the relative path that gives the cam_id and date, and the file
# name.
# Parameters: the absolute path to the video, and 
# the location of the airvision Videos directory.
# Return: The relative path that gives the cam id
# and date (camera_id/2013/10/12/12)
# and the file name of the video.
def date_and_file_name(abs_path, airVision_videos):
    abs_path_partition = abs_path.partition(airVision_videos)
    rel_path = abs_path_partition[2].encode('ascii')
    path_and_name = os.path.split(rel_path)
    return path_and_name[0], path_and_name[1]



