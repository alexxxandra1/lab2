### Такс микрогайд по многоуровневму прицептрону  
Тут не будет всякой теории вы сами можете выитать и тп.
1. Вообще главные моменты для запуска, поскольку у всех по раному сделаны датасеты, то вам надо будет под себя переписать  
открытие датасета под себя, хранится функция для открытия датасета в /utils/ , там что то вроде matrix_csv_loader, просто если у вас идет сначала матрица пикселей а потом идет класс, то у вас как у меня и будет работать,
если сначала класс а потом уже матрица пикселей, то препишите
3. ```bash
   cd ui
   python ApplicationFrame.py
   ```
4. вводите скорость обучения где-то 0.2, и количчество эпох где-то 7, и потом может рисовать распозновать
5. Советую переделать интерфейс, хотя бы кнопки переставить там в формате grid можете прочитать что это такое, там все просто, ну типо переставтье кнопки, можете их еще покрасить,
и в поля ввода добавить валидацию
6. Для шарящих советую еще убрать части хардкода моего, ночью писал и там прям видно, что много нахардкожено
7. Вообще вся суть хранится в /core там класс перцептрона, и классы для нейрона и слоев, из нейронов
8. Не знаю честно говоря что рассказывать, по вопросам пишите в личку, просто, обьясню лично  
#### Описание проекта:  
/activasion/ -функция активации  
/configayration/ - конфигруация перцептрона  
/core/ - основная логика слои, нейрон и сам перцептрон  
/domain/ - крч утилиты для сравнения  
/loss/ - функция потерь  
/metrics/ - метрихи эпохи обучения  
/ui/ - интерфейс  
/utils/ - загрузка данных из датасета  