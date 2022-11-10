# windows_fs_to_csv
This script scrapes windows from C:\, unless other location specified and adds paths, filenames, extension and different metadata too and stores it as a csv.  I thought, why not make it public? I'm using this as a standalone tool for another larger project.




# To make it into a standalone executable:

    pip install pyinstaller
    
Installs pyinstaller


    pyinstaller yourprogram.py
This will generate the bundle in a subdirectory called dist.

    pyinstaller -F yourprogram.py
Packs everything into single executable.

    pyinstaller -F --paths=<your\_path>\Lib\site-packages  yourprogram.py
