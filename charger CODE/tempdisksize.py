import shutil
import glob
import os

total, used, free = shutil.disk_usage("/")
print ("Total: %d GB" % (total // ( 2**30)))
print ("Used: %d GB" % (used // ( 2**30)))
print ("Free: %d GB" % (free // ( 2**30)))

files = glob.glob("*.py")
files.sort(key=os.path.getmtime)
os.remove
print("\n".join(files))
