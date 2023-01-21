import re
import sys
import os
import time
from multiprocessing import Pool

from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QFileDialog, QApplication, QMessageBox
from qt_material import apply_stylesheet, QtStyleTools
from qt.ui_form import Ui_Form
from qt.qt_service import start_html, get_result_html, get_matrix_from_file, write_results
from matriсes.berlin_52 import now_matrix as berlin_52_matrix
from matriсes.eil_76 import now_matrix as eil_76_matrix
from matriсes.bays_29 import now_matrix as bays_29_matrix


from base_selection import TournamentSelection
from base_individual import IndividualWithFormedInitialGenes

from models.goldberg.goldberg_with_2_generation import GoldbergWithTwoGeneration
from models.goldberg.simple_goldberg import Goldberg

from representations.travel_representation.crossover import OrderedCrossover, ChangesCrossover
from representations.travel_representation.fitness_function import travel_fitness_function
from representations.travel_representation.mutation import MutationExchange

from representations.ordinal_representation.individual import OrdinalIndividualWithFormedInitialGenes
from representations.ordinal_representation.fitness_function import ordinal_fitness_function
from representations.ordinal_representation.mutation import SinglePointOrdinalMutation
from representations.ordinal_representation.crossover import SinglePointCrossover


class GoldbergWidget(QWidget, Ui_Form, QtStyleTools):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.matrix_file_name = ''
        self.result_file_name = ''
        self.results = []

        self.matrix_dict = {
            'bays29': bays_29_matrix,
            'berlin52': berlin_52_matrix,
            'eil76': eil_76_matrix
        }

        self.model_dict = {
            'Одноэтапная модель': Goldberg,
            'Двухэтапная модель': GoldbergWithTwoGeneration
        }
        self.crossover_dict = {
            'Упорядоченный кроссовер': OrderedCrossover,
            'Изменённый кроссовер': ChangesCrossover,
            'Одноточечный кроссовер': SinglePointCrossover
        }

        self.evr_dict = {
            '№1. По минимальному маршруту': '1',
            '№2. По максимальному маршруту': '2',
            '№3. По случайному маршруту': '3'
        }
        self.representation_dict = {
            'Путевое представление': IndividualWithFormedInitialGenes,
            'Порядковое представление': OrdinalIndividualWithFormedInitialGenes
        }

    def setupUi(self, Form):
        super(GoldbergWidget, self).setupUi(self)
        self.comboBox_matrix.addItems(["bays29", "berlin52", "eil76", "Другой вариант"])
        self.comboBox_model.addItems(["Одноэтапная модель", "Двухэтапная модель"])
        self.comboBox_evr.addItems([
            "№1. По минимальному маршруту",
            "№2. По максимальному маршруту",
            "№3. По случайному маршруту",
            "Другой вариант"
        ])
        self.comboBox_representation.addItems(["Путевое представление", "Порядковое представление"])

        self.comboBox_matrix.setCurrentIndex(1)
        self.add_choices_to_travel_representation()

        self.comboBox_matrix.setStyleSheet("""font-size:17px;""")
        self.comboBox_model.setStyleSheet("""font-size:17px;""")
        self.comboBox_evr.setStyleSheet("""font-size:17px;""")
        self.comboBox_representation.setStyleSheet("""font-size:17px;""")
        self.comboBox_crossover.setStyleSheet("""font-size:17px;""")

        self.comboBox_matrix.activated[str].connect(self.on_activated_comboBox_matrix)
        self.comboBox_model.activated[str].connect(self.on_activated_comboBox_model)
        self.comboBox_representation.activated[str].connect(self.on_activated_comboBox_representation)
        self.comboBox_evr.activated[str].connect(self.on_activated_comboBox_evr)

        self.launch_count.setStyleSheet("""font-size:17px;""")
        self.generation_size_1.setStyleSheet("""font-size:17px;""")
        self.repeat_count_1.setStyleSheet("""font-size:17px;""")
        self.generation_size_2.setStyleSheet("""font-size:17px;""")
        self.repeat_count_2.setStyleSheet("""font-size:17px;""")
        self.p_crossover.setStyleSheet("""font-size:17px;""")
        self.p_mutation.setStyleSheet("""font-size:17px;""")
        self.lineEdit_evr.setStyleSheet("""font-size:17px;""")

        self.launch_count.setRange(1, 100)
        self.generation_size_1.setRange(2, 5000)
        self.repeat_count_1.setRange(1, 5000)
        self.generation_size_2.setRange(2, 5000)
        self.repeat_count_2.setRange(1, 5000)
        self.p_crossover.setRange(0, 100)
        self.p_mutation.setRange(0, 100)

        self.launch_count.setValue(10)
        self.generation_size_1.setValue(10)
        self.repeat_count_1.setValue(10)
        self.generation_size_2.setValue(10)
        self.repeat_count_2.setValue(10)
        self.p_crossover.setValue(100)
        self.p_mutation.setValue(100)

        self.pushButton_2.hide()
        self.hide_label_for_2_generation()
        self.lineEdit_evr.hide()

        self.matrix_file_name = ""
        self.pushButton.clicked.connect(self.run)
        self.pushButton.setProperty('class', 'blue_btn')
        self.pushButton_3.setProperty('class', 'blue_btn')

        self.pushButton_2.clicked.connect(self.open_matrix_file)
        self.pushButton_3.clicked.connect(self.open_result_file)

    def on_activated_comboBox_matrix(self, text):
        """ Обработка выбора матрицы"""
        if text == 'Другой вариант':
            self.pushButton_2.show()
        else:
            self.pushButton_2.hide()

    def on_activated_comboBox_model(self, text):
        """ Обработка выбора модели"""
        if text == "Двухэтапная модель":
            self.show_label_for_2_generation()
        else:
            self.hide_label_for_2_generation()

    def show_label_for_2_generation(self):
        """ Показать дополнительные поля ввода для параметров двухэтапной модели"""
        self.generation_size_2.show()
        self.repeat_count_2.show()
        self.label_5.show()
        self.label_6.show()

    def hide_label_for_2_generation(self):
        """ Спрятать дополнительные поля ввода для параметров двухэтапной модели"""
        self.generation_size_2.hide()
        self.repeat_count_2.hide()
        self.label_5.hide()
        self.label_6.hide()

    def on_activated_comboBox_representation(self, text):
        """ Обработка выбора представления"""
        if text == 'Путевое представление':
            self.add_choices_to_travel_representation()
        else:
            self.add_choices_to_ordinal_representation()

    def on_activated_comboBox_evr(self, text):
        """ Обработка выбора эвристического алгоритма для формирования начального поколения"""
        if text == 'Другой вариант':
            self.lineEdit_evr.show()
        else:
            self.lineEdit_evr.hide()

    def add_choices_to_travel_representation(self):
        """ Добавление кроссоверов путевого представления в поле выбора"""
        self.comboBox_crossover.clear()
        self.comboBox_crossover.addItems(["Упорядоченный кроссовер", "Изменённый кроссовер"])

    def add_choices_to_ordinal_representation(self):
        """ Добавление кроссоверов порядкового представления в поле выбора"""
        self.comboBox_crossover.clear()
        self.comboBox_crossover.addItems(["Одноточечный кроссовер"])

    def open_matrix_file(self):
        """ Выбор файла c матрицей"""
        file_name, _ = QFileDialog.getOpenFileName(self, 'Выберете файл с матрицей городов', r".",
                                                       "Текстовые файлы (*.txt)")
        if file_name.split('/')[-1]:
            self.pushButton_2.setText(file_name.split('/')[-1])
            self.matrix_file_name = os.path.normpath(file_name)

    def open_result_file(self):
        """ Выбор файла для сохранение результата """
        file_name, _ = QFileDialog.getOpenFileName(self, 'Выберете файл для сохранения результата', r".",
                                                       "Текстовые файлы (*.txt)")
        if not file_name:
            return
        self.pushButton_2.setText(file_name.split('/')[-1])
        self.result_file_name = os.path.normpath(file_name)
        msg = QMessageBox()
        if not self.results:
            msg.setWindowTitle("Ошибка")
            msg.setText(f"Результаты работы ГА отсутствуют!")
            msg.setIcon(QMessageBox.Critical)
        else:
            write_results(self.result_file_name, self.results, self.running_time)
            msg.setWindowTitle("Уведомление")
            msg.setText(f"Результаты работы ГА записаны в файл \n{self.result_file_name}")
            msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def run(self):
        """ Обработка нажатие клавишии 'Запуск ГА' """
        mutation, fitness_function = self.get_fitness_function_and_mutation()
        try:
            matrix = self.get_matrix()
            key = self.get_key()
        except ValueError as err:
            return

        self.pushButton.setEnabled(False)
        QtWidgets.qApp.processEvents()

        individual_type = self.representation_dict[self.comboBox_representation.currentText()]
        mutation_probability = self.p_mutation.value()
        crossover_probability = self.p_crossover.value()
        model = self.model_dict[self.comboBox_model.currentText()]
        generation_size = self.generation_size_1.value()
        number_of_repetitions = self.repeat_count_1.value()
        crossover_type = self.crossover_dict[self.comboBox_crossover.currentText()]
        first_generation_params = dict(
            number_of_repetitions=number_of_repetitions,
            generation_size=generation_size,
            mutation_probability=mutation_probability,
            crossover_probability=crossover_probability,
            matrix=matrix,
            individual_type=individual_type,
            mutation_type=mutation,
            crossover_type=crossover_type,
            selection_type=TournamentSelection,
            fitness_function=fitness_function,
            individual_params={'matrix': matrix, 'key': key}
        )

        started_at = time.time()
        if self.comboBox_model.currentText() == "Двухэтапная модель":
            generation_size_2 = self.generation_size_2.value()
            number_of_repetitions_2 = self.repeat_count_2.value()
            goldberg = model(
                first_generation_model=Goldberg,
                first_generation_params=first_generation_params,
                number_of_repetitions=number_of_repetitions_2,
                generation_size=generation_size_2,
                mutation_probability=mutation_probability,
                crossover_probability=crossover_probability,
                matrix=matrix,
                individual_type=individual_type,
                mutation_type=mutation,
                crossover_type=crossover_type,
                selection_type=TournamentSelection,
                fitness_function=fitness_function,
                individual_params={'matrix': matrix, 'key': key}
            )
            self.results = []
            for i in range(self.launch_count.value()):
                res = start_ga(goldberg)
                self.results.append(res)
        else:
            goldberg = model(**first_generation_params)
            pool = Pool()
            pool_lists = [goldberg for i in range(self.launch_count.value())]
            self.results = list(pool.map(start_ga, pool_lists))
            pool.terminate()
        self.results.sort(key=lambda x: x[1])
        ended_at = time.time()
        html = start_html
        self.textBrowser.insertHtml(html)
        for index, element in enumerate(self.results):
            html += get_result_html(index, element)
        self.running_time = round((ended_at - started_at) / 60, 2)
        html += f"<h3>Время работы алгоритма:  {self.running_time} минут(ы)</h3>"
        html += f"<body>"
        self.textBrowser.setHtml(html)
        font = QFont('Roboto')
        font.setPixelSize(18)
        self.textBrowser.setFont(font)
        self.tabWidget.setCurrentIndex(1)
        self.pushButton.setEnabled(True)

    def get_key(self):
        """ Получение ключа (распределение эвристического алгоритма для формирования начального поколения)"""
        if self.comboBox_evr.currentText() == 'Другой вариант':
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            if not self.lineEdit_evr.text():
                msg.setText("Вы не ввели эвристический алгоритм для формирования начального поколения")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                raise ValueError('ошибка')
            else:
                pattern = re.compile(r'^[1-3]+$')
                if not pattern.fullmatch(self.lineEdit_evr.text()):
                    msg.setText(f"Вы не правильно задали эвристический алгоритм для формирования начального поколения!\n"
                                f"Алгоритм должен содержать одну из следующих цифр: 1,2,3 или их комбинацию.\n"
                                f"Примеры комбинаций: 123, 111222333")
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()
                    raise ValueError('ошибка')
                return self.lineEdit_evr.text()
        else:
            key = self.evr_dict[self.comboBox_evr.currentText()]
            return key

    def get_fitness_function_and_mutation(self):
        """ Получение функции приспособленнсти и мутации"""
        if self.comboBox_representation.currentText() == 'Путевое представление':
            mutation = MutationExchange
            fitness_function = travel_fitness_function
        else:
            mutation = SinglePointOrdinalMutation
            fitness_function = ordinal_fitness_function
        return mutation, fitness_function

    def get_matrix(self):
        """ Получение матрицы"""
        if self.comboBox_matrix.currentText() == 'Другой вариант':
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            if not self.matrix_file_name:
                msg.setText("Вы не выбрали файл с задачей!")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                raise ValueError('Вы не выбрали файл с задачей')
            else:
                try:
                    matrix = get_matrix_from_file(self.matrix_file_name)
                except ValueError as err:
                    msg.setText(f"Вы не правильно задали ввели матрицу!\n{err}")
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()
                    raise
        else:
            matrix = self.matrix_dict[self.comboBox_matrix.currentText()]
        return matrix


def start_ga(goldberg):
    """ Запуск ГА"""
    return goldberg.start_genetic_algorithms()


def create_window():
    """ Создание и запуск оконного приложения"""
    app = QApplication(sys.argv)
    window = GoldbergWidget()
    extra = {
        # Font
        'font_family': 'Roboto',
        'font_size': '11px'
    }
    apply_stylesheet(app, theme='dark_blue.xml', extra=extra)
    stylesheet = app.styleSheet()
    with open(r'custom.css') as file:
        app.setStyleSheet(stylesheet + file.read().format(**os.environ))
    window.show()
    app.exec_()


def main():
    create_window()


if __name__ == '__main__':
    main()
