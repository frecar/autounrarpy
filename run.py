import os, sys, time, platform, ctypes, shutil
from stat import *
from heapq import *

BASE_PATH = os.path.dirname(__file__)
if BASE_PATH:
    BASE_PATH += "/"


def add_file_to_unrared_list(filename):
    f = open(BASE_PATH + "UNRARED_FILES.txt", "a")

    if len(str(filename).strip()):
        f.write(time.ctime() + " ")
        f.write(filename)
        f.write("\n")

    f.close()


def filename_in_unrared_files(filename):
    try:
        f = open(BASE_PATH + "UNRARED_FILES.txt", "r")
        result = filename in f.read()
        f.close()
        return result
    except Exception:
        return False


def find_rar_files(folder):
    rar_files = []

    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            if '.rar' in filename and '.part' not in filename:
                if not filename_in_unrared_files(filename):
                    rar_files.append(filename)
                    add_file_to_unrared_list(filename)

    return rar_files


def free_space(folder):
    # Return folder/drive free space (in bytes)
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value
    else:
        folder_stat = os.statvfs(folder)
        return folder_stat.f_bavail * folder_stat.f_frsize


def walk_flat_file(top, callback):
    for f in os.listdir(top):
        callback(os.path.join(top, f))


def visitfile(file):
    print '%s created: %s' % (file, creation_time(file))


def creation_time(path):
    return os.stat(path)[ST_CTIME]


def build_heap(root_path):
    heap = []
    for f in os.listdir(root_path):
        path = os.path.join(root_path, f)
        heappush(heap, (creation_time(path), path))
    return heap


def is_directory(path):
    return S_ISDIR(os.stat(path)[ST_MODE])


def delete_thing(path):
    if is_directory(path):
        shutil.rmtree(path)
    else:
        os.remove(path)


def enough_free_space(root_path, required_bytes):
    return free_space(root_path) >= required_bytes


def folder_of_filename(filename):
    new_filename = ""

    for part in filename.split(os.sep)[:len(filename.split(os.sep)) - 1]:
        new_filename += part + os.sep

    return new_filename


def main(media_path, required_gigabytes):
    required_bytes = int(required_gigabytes) * (1000 * 1000 * 1000)

    logg = open(BASE_PATH + "DELETE_LOG.txt", "a")

    if not enough_free_space(media_path, required_bytes):
        heap = build_heap(media_path)
        logg.write("\n\n")
        logg.write(time.ctime() + " Need more space, commencing search \n")
        while not enough_free_space(media_path, required_bytes) and len(heap) > 0:
            logg.write(time.ctime() + " Deleting " + str(heap[0][1]) + ", thereby gaining " + str(
                free_space(media_path)) + " bytes of free space.\n")
            delete_thing(heappop(heap)[1])
        if enough_free_space(media_path, required_bytes):
            logg.write(time.ctime() + " Finished with enough free space.\n")
        else:
            logg.write(time.ctime() + " Didn't free up as much as desired \n")

    logg.close()

    for rar_file in find_rar_files(media_path):
        #os.system("cd '" + folder_of_filename(rar_file) + "'")
        os.system("unrar x '" + rar_file + "' '" + folder_of_filename(rar_file) + "'")


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])