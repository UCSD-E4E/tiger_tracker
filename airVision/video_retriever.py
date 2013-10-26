import os

# Returns a list of all the airvision video 
# directories (2013/10/22/13, 2013/10/22/14...) 
# below the Videos directory
# Paramters: path to the Videos directory
# (For example:
# "/Programdata/airvision/data/camera/videos")
# Return: a list with the relative paths to
# the video directories, and a list with their
# absolute paths
def grab_video_dirs(path):
    video_dirs_rel = []  
    video_dirs_abs = []  
    
    for root, dirs, files in os.walk(path):
        # only collect directories pointing to the hour folder: e.g. 2013/10/22/13        
        rel_path = os.path.relpath(root,path)
        if rel_path.count("/") == 3:        
            video_dirs_abs.append(root)
            video_dirs_rel.append(rel_path)
    
    return video_dirs_rel, video_dirs_abs


# Paramters: processed_until: The relative path of the last video 
# directory processed ( 2013/10/24/16 for example)
# rel_paths: a list with the relative paths of all directories
# abs_paths: a list with the absolute paths of all directories
# Return a list with absolute paths to directories that are
# greater (temporally) to the processed_until directory
def to_process(processed_until, rel_paths, abs_paths):
    need_processing = []
    for i in range(0, len(rel_paths)):
        if rel_paths[i] > processed_until:
            need_processing.append(abs_paths[i])
    return need_processing

