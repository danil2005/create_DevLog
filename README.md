# Оформление прошивок для передачи на тестирование

Данный инструмент разработан на языке Python и предназначен для автоматизации процесса подготовки пакета прошивок к передаче на тестирование. Скрипт выполняет несколько ключевых задач: рассчитывает контрольные суммы (CRC), формирует текстовый файл с технической информацией (DevLog), упаковывает прошивки и все необходимые файлы в структурированный архив.

## Установка необходимых компонентов

Проект разработан на языке программирования **Python**. Для корректной работы скрипта рекомендуется использовать Python версии **3.13** или выше, так как проект был протестирован и оптимизирован именно под эту версию.

Для корректной работы скрипта необходимо установить Python-модули, для этого выполните команду:  

```bash
pip install crcmod intelhex PyQt5
```

Также можно установить все зависимости из файла, выполнив следующую команду из директории проекта:

```bash
pip install -r requirements.txt
```

## Конфигурация


Перед использованием необходимо настроить параметры для каждой прошивки в файле `settingsDevLog.json`. Файл содержит массив JSON-объектов со следующей структурой:

```json
{
    "Name": "firmware_1",
    "Name_board": "board_1",
    "Module": "module_1",
    "MCU": "MCU_1",
    "Start": "0x0",
    "End": "0x100",
    "Start_boot": "0x200",
    "End_boot": "0x300",
    "Folder": "folder_1"
}
```

Поля объекта:  
`Name` - название прошивки без `.hex`;  
`Name_board` - название платы, для которой скомпилирована прошивка;  
`Module` - название модуля связи, который используется в плате;  
`MCU` - название микроконтроллера;  
`Start` - адрес начала основной части прошивки для расчета  CRC;  
`End` - адрес конца основной части прошивки для расчета  CRC;  
`Start_boot` - адрес начала части bootloader для расчета CRC;  
`End_boot` - адрес конца части bootloader для расчета CRC;  
`Folder` - папка, в которую будет помещена прошивка в архиве.  

В репозитории уже присутствует файл `settingsDevLog.json`. Отредактируйте его в соответствии с вашими данными.

## Как пользоваться

1. Настройте свою IDE таким образом, чтобы прошивки сохранялись в директории проекта. Либо вручную скопируйте скомпилированные прошивки.

2. Запустите файл `interface.py`. Откроется окно с графическим интерфейсом.

3. Заполните поля `Изменения` и `Версия`. Введенная ифнормация будет использована в названии архива, а также при генерации `DevLog.txt`.

4. Нажмите кнопку `Старт` , чтобы начать обработку. По завершении будет создан архив, содержащий прошивки, организованные по соответствующим папкам и сгенерированный файл `DevLog.txt`. В окне интерфейса отобразится количество успешно обработанных и пропущенных прошивок.

5. Скомпилируйте прошивки для проверки обновления и нажмите кнопку `Старт NOP`. Прошивки будут находится в папке `Прошивки для проверки обновления`. В окне интерфейса отобразится количество обработанных и пропущенных прошивок.

6. После завершения всех операций нажмите кнопку Добавить изменения в файл . Если в директории отсутствует файл со сквозным описанием изменений, он будет создан и добавлен в архив. По завершении процесса в окне отобразится сообщение Готово .

## Демострация работы

В папке `fw_for_test` есть набор прошивок по которым составлены настройки в файле `settingsDevLog.json`. Вы можете использовать эти прошивки чтобы опробовать скрипт в действии.

## Автор

Потапенков Данил Валерьевич  
+79964188236  
danil2000p@yandex.ru  






