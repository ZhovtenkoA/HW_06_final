import os
import re
import sys
import shutil
import zipfile
from pathlib import Path

def normalize_name(name: str) -> str:
    CYRILIC = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    LATIN = (
        "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
        "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja")
    TRANS = {}
    for c, l in zip(CYRILIC, LATIN):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    n_name = name.translate(TRANS)
    n_name = re.sub(r'W/', '_', n_name)
    return n_name

directions = {
    'images' : ['.jpeg', '.png', '.jpg', '.svg'], 
    'video' : ['.avi', '.mp4', '.mov', '.mkv'], 
    'documents' : ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'], 
    'audio': ['.mp3', '.ogg', '.wav', '.amr'], 
    'archives' : ['.zip', '.gz', '.tar'],
    'others' : []
}

sorting_direction = Path('d:/HW_06/a') #sys.argv[1]


def remove_dirs(direction_list):
    for dir_p in reversed(direction_list):
        if os.path.split(dir_p)[1] in directions or os.stat(dir_p).st_size != 0:
            continue
        else:
            os.rmdir(dir_p)
                
def sorting(sorting_direction):
    current_dir = Path(sorting_direction)
    direction_list = []
    known_extensions, unknown_extensions = set(), set()

    for way, dirs, files in os.walk(sorting_direction):
        for d in dirs:
            if not d:
                continue
            direction_list.append(os.path.join(way, d))
        for file in files:
            file_path = Path(way) / file
            normal_name = f"{normalize_name(file_path.name[0:-len(file_path.suffix)])}{file_path.suffix}"
            file_path.rename(Path(way) / normal_name)
            file_path = Path(way) / normal_name
            for suffixes in directions:
                if file_path.suffix.lower() in directions[suffixes]:
                    add_direction = current_dir / suffixes
                    add_direction.mkdir(exist_ok=True)
                    if os.path.exists(file_path):
                        file_path.rename(add_direction.joinpath(file_path.name))
                        known_extensions.add(file_path.suffix)
                        if file_path.suffix.lower() == '.zip':
                            known_extensions.add(file_path.suffix)
                            with zipfile.ZipFile(add_direction.joinpath(file_path.name), mode="r") as archive:
                                for file in archive.namelist():
                                    archive.extract(file, add_direction/file_path.name[0:-len(file_path.suffix)])
                                    arch_to_del = Path(
                                        add_direction.joinpath(file_path.name))
                            arch_to_del.unlink()
                        elif file_path.suffix.lower() in ['.gz', '.tar']:
                            known_extensions.add(file_path.suffix)
                            shutil.unpack_archive(
                                file_path, add_direction/file_path.name[0:-len(file_path.suffix)])
                            file_path.unlink()
            for suffixes in directions:
                if file_path.suffix.lower() not in directions[suffixes]:
                    add_direction = current_dir / 'others'
                    add_direction.mkdir(exist_ok=True)
                    if os.path.exists(file_path):
                        file_path.rename(
                            add_direction.joinpath(file_path.name))
                        unknown_extensions.add(file_path.suffix)
                        
               
    remove_dirs(direction_list)
    return list(known_extensions), list(unknown_extensions)
                
            


if __name__ == "__main__":
    sorting_direction = Path(sys.argv[1])  # sys.argv[1]
    if not Path(sorting_direction).exists():
        print('Путь не найден')
    else:
        known, unknown = sorting(sorting_direction)
    print('Сортировка окончена')
    if len(known) >= 0:
        print(f"\nРаспознанные расширения:\n{known}")
    if len(unknown) >= 0:
        print(f"Не распознанные расширения:\n{unknown}")
    



