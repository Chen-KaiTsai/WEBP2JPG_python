# Author : Chen-Kai Tsai
# Please invoke this python script directly

from PIL import Image
import time
import sys
import os
import multiprocessing

# Global variable
convert_path = ""

def WEBP2JPG(webp_img):
    filename = os.path.join(dir_path, webp_img)
    img = Image.open(filename)
    if img.mode == "RGBA":
        img.load()
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
    savepath = os.path.join(convert_path, webp_img)
    savename = savepath.replace("webp", "jpg")
    img.save("{}".format(savename), "JPEG")

argc = len(sys.argv)

print("Python Script : " + sys.argv[0] + " Start.")

if argc != 3:
    print("Error : Script Requir ONE arg as TOP DIR Path and ONE arg as Number of Process Invoke (0 to use system parameter)")
    exit()

dir_path = sys.argv[1]
n_processes = int(sys.argv[2])

if n_processes == 0:
    n_processes = multiprocessing.cpu_count()

# Read and list all file name in the dir with .webp extension
print("Working on dir : " + dir_path + "\n\n")

files = os.listdir(dir_path)
print("-" * 64)
print("The total number of files in the directory : " + str(len(files)))
print("-" * 64 + "\n\n")

print("-" * 64)
webp_files = [x for x in files if x.endswith(".webp")]
print("The total number of .webp files in the directory : " + str(len(webp_files)))
print("-" * 64 + "\n\n")

# Create convert dir
convert_dir = "converted"
convert_path = os.path.join(dir_path, convert_dir)

try:
    os.makedirs(convert_path)
    print("Directory \"" + convert_dir + "\" created")
except OSError as error:
    print("Directory \"" + convert_dir + "\" already exist")

# Reference : https://www.jianshu.com/p/f04a8531b4de
# Multiprocessing to transfer all .webp file to .jpg

starttime = time.time()

pool = multiprocessing.Pool(processes=n_processes)

pool.map(WEBP2JPG, webp_files)

endtime = time.time()

print("--- %s seconds ---" % (endtime - starttime))
