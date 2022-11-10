import csv
import os
import hashlib
import subprocess

location = str(input("Location to scan from (if blank - defaults to: C:\\):"))
if location.strip(" ") == "":
    location = "C:\\"


def file_hasher(file_to_hash):
    try:
        with open(file_to_hash, "rb") as current:
            readfile = current.read() + bytes(file_to_hash, "utf-8")
            return hashlib.md5(readfile).hexdigest()
    except Exception as Argument:
        f = open("logging.txt", "a")
        f.write(str(Argument))
        f.close()
        return ""


def file_hasher_sha(file_to_hash):
    try:
        with open(file_to_hash, "rb") as current:
            readfile = current.read() + bytes(file_to_hash, "utf-8")
            return hashlib.sha256(readfile).hexdigest()
    except Exception as Argument:
        f = open("logging.txt", "a")
        f.write(str(Argument))
        f.close()
        return ""


def run_ps(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
    return completed.stdout


# counter = 0

with open('temp.csv', 'wt', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(("ParentDirectoryName", "Name", "FullName", "Extension", "Length",
                     "Attribute", "MD5", "SHA256", "sddl", "Information", "Tags"))

    parentDirName = ""
    name = ""
    fullName = ""
    extension = ""
    length = int
    attribute = ""
    MD5 = ""
    SHA256 = ""
    sddl = ""
    information = ""
    tags = ""
    row = (parentDirName, name, fullName, extension, length, attribute, MD5, SHA256, sddl, information, tags)
    for (dirpath, dirnames, filenames) in os.walk(location):
        try:
            parentDirName = str(dirpath.split("\\")).replace("\\\\","\\")
            parentDirName = "\\".join(parentDirName[:-2])

            name = dirpath.split("\\")
            if dirpath == "C:\\":
                name = "C:\\"
            else:
                name = name[-1]

            extension = "dir"
            MD5 = ""
            SHA256 = ""
            sddl = run_ps("Get-Acl '{}' | Select -ExpandProperty Sddl".format(dirpath)).strip("\n")
            information = ""
            tags = ""
            length = 0
            attribute = "{0}".format(os.stat(dirpath).st_file_attributes)
            fullName = dirpath.replace("\\\\", "\\")
            row = (parentDirName, name, fullName, extension, length, attribute, MD5, SHA256, sddl, information, tags)
            writer.writerow(row)
            for file in filenames:
                parentDirName = dirpath.replace("\\\\", "\\")
                name = file
                if dirpath == "C:\\":
                    fullName = dirpath + file
                else:
                    fullName = dirpath.replace("\\\\", "\\") + "\\" + file
                extension = file.split(".")[-1]
                length = os.path.getsize(fullName)
                attribute = "{0}".format(os.stat(fullName).st_file_attributes)
                MD5 = file_hasher(fullName)
                SHA256 = file_hasher_sha(fullName)
                sddl = run_ps("Get-Acl '{}' | Select -ExpandProperty Sddl".format(fullName)).strip("\n")
                information = ""
                tags = ""
                row = (
                parentDirName, name, fullName, extension, length, attribute, MD5, SHA256, sddl, information, tags)
                writer.writerow(row)
            #     counter += 1
            #     if counter >= 10000:
            #         break
            # counter += 1
        except Exception as Argument:
            f = open("logging.txt", "a")
            f.write(str(Argument))
            f.close()
