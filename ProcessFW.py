import json
from datetime import datetime
import crcmod
from zipfile import ZipFile
from os import remove, path
from concurrent.futures import ProcessPoolExecutor, as_completed
from intelhex import IntelHex


class Firmwares:
    def __init__(self, parameters: dict) -> None:
        self.name = parameters["Name"]
        self.name_file = parameters["Name"] + ".hex"
        if not path.isfile(self.name_file):
            raise ValueError("The file is not in the directory")
        self.name_board = parameters["Name_board"]
        self.module = parameters["Module"]
        self.MCU = parameters["MCU"]
        self.start = int(parameters["Start"], base=16)
        self.end = int(parameters["End"], base=16)
        self.start_boot = int(parameters["Start_boot"], base=16)
        self.end_boot = int(parameters["End_boot"], base=16)
        self.folder = parameters["Folder"]
        self.type_PIC = True if self.MCU.startswith("PIC") else False

        # обрабатываем прошивку
        dump = self.get_dump_hex_file()

        ID_ADDR = 0x50
        ROLE_ADDR = 0x60

        ID_ADDR_PIC = 0x70
        ROLE_ADDR_PIC = 0x80

        if self.type_PIC:
            self.id = dump[ID_ADDR_PIC]
            self.role = dump[ROLE_ADDR_PIC]
        else:
            self.id = dump[ID_ADDR]
            self.role = dump[ROLE_ADDR]

        self.crc16_main = self.crc16_func(dump[self.start : self.end])
        self.crc16_boot = self.crc16_func(dump[self.start_boot : self.end_boot])

    def get_dump_hex_file(self):
        """Функция фозвращает спсиок сырых данных hex-файла"""
        ih = IntelHex()
        ih.loadhex(self.name_file)
        dump = ih.tobinarray()
        if self.type_PIC:
            for i in range(3, len(dump), 4):
                dump[i] = 0
        return dump

    @staticmethod
    def crc16_func(data):
        """Метод подсчитывает CRC16 заданного массива"""
        return crcmod.mkCrcFun(0x11021, rev=False, initCrc=0xFFFF, xorOut=0x0000)(data)

    def add_zip_archive(self, zip_name: str, is_nop: bool):
        """Добавляет файл в архив"""
        with ZipFile(zip_name, mode="a") as zip_file:
            folder = self.folder if not is_nop else "Прошивки для проверки обновления"
            if folder == None:
                zip_file.write(self.name_file, self.name_file)
            else:
                zip_file.write(self.name_file, f"{folder}/{self.name_file}")

    def delete_from_directory(self):
        remove(self.name_file)

    def __str__(self) -> str:
        pattern = """{}
CRC: {}
Boot CRC: {}
ID: {}
Role: {}
Передаточное число: отсутствует
Module: {}
MCU: {}"""

        return pattern.format(
            self.name,
            f"0x{self.crc16_main:04X}",
            f"0x{self.crc16_boot:04X}",
            f"0x{self.id:02X}",
            f"0x{self.role:02X}",
            self.module,
            self.MCU,
        )


def parsing_fw(version: str, changes: str, is_nop: bool = False):
    """Функция обрабатывает прошивки, составляет DevLog и добавляет прошивки в архив, удаляя из директории"""

    with open("settingsDevLog.json") as file:
        setings = json.load(file)

    cnt_fault = 0
    obj_firmwares = []

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(Firmwares, i) for i in setings]
        for future in as_completed(futures):
            try:
                obj = future.result()
                obj_firmwares.append(obj)
                obj.add_zip_archive(f"Шлюзы {version}.zip", is_nop)
                obj.delete_from_directory()
            except:
                cnt_fault += 1

    # for i in setings:
    #     try:
    #         obj = Firmwares(i)
    #         obj_firmwares.append(obj)
    #         obj.add_zip_archive(f'Шлюзы {version}.zip', is_nop)
    #         obj.delete_from_directory()
    #     except:
    #         cnt_fault += 1

    with open("DevLog.txt", "w", encoding="utf8") as file:
        # добавляем шапку
        if not is_nop:
            print(
                f'Прошивки для шлюзов на платах {", ".join(sorted(list(set(map(lambda x: x.name_board, obj_firmwares)))))}',
                file=file,
            )
            print(f"Версия - {version}", file=file)
            print(
                f'Тип процессора {", ".join(sorted(list(set(map(lambda x: x.MCU.split()[0], obj_firmwares)))))}',
                file=file,
            )
            print("------------------------------------", file=file)
            print(datetime.now().strftime("%d.%m.%Y %H:%M:%S,%f")[:-4], file=file)

        print(
            "\n".join(
                map(lambda x: f"\n{x[0]}. {x[1]}", enumerate(obj_firmwares, start=1))
            ),
            file=file,
        )

        if not is_nop:
            print(f"\nВерсия {version}\nИзменения:\n{changes}", file=file)

    with ZipFile(f"Шлюзы {version}.zip", mode="a") as zip_file:
        if not is_nop:
            zip_file.write("DevLog.txt", "DevLog.txt")
        else:
            zip_file.write("DevLog.txt", "Прошивки для проверки обновления/DevLog.txt")

    remove("DevLog.txt")

    return len(obj_firmwares), cnt_fault


def save_changes_to_file(version: str, changes: str):
    """Добавляет изменения в файл с историей всех изменений"""
    with open("Изменения в шлюзах.txt", "a", encoding="utf-8") as file:
        print(file=file)
        print(f"Версия {version}\nИзменения:\n{changes}", file=file)

    with ZipFile(f"Шлюзы {version}.zip", mode="a") as zip_file:
        zip_file.write("Изменения в шлюзах.txt", "Изменения в шлюзах.txt")
