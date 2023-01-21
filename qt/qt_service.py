start_html = """               <html>
           <head>
           <style>
           .result__container{
                      margin-left: 45px ;

            }
            .result__key{
                color: white
            }
            .result__h{
                margin-bottom: 15px;
                margin-top: 30px;
            }
            </style>
           </head>
           <body>
           """

def get_result_html(index, element):
    generation, value, individual = element
    individual = ' '.join([str(gen) for gen in individual])
    text = f'<h3 class="result__h">Результат №{index + 1}</h3>' \
           f'<div class="result__container">' \
           f'<p><span class="result__key">Поколение: </span> <span class="result__value">{generation}</span></p>' \
           f'<p><span class="result__key">Значение: </span> <span class="result__value">{value}</span></p>' \
           f'<p><span class="result__key">Особь: </span> <span class="result__value">{individual}</span></p>' \
           f'</div>'
    return text


def get_matrix_from_file(file_name):
    with open(file_name, 'r', encoding='utf8') as f:
        try:
         matrix = [list(map(float, row.split())) for row in f.readlines()]
        except Exception as e:
            raise ValueError('Не корректные значения у элементов матрицы')
        check_matrix(matrix)
        return matrix


def check_matrix(matrix):
    len_matrix = len(matrix)
    for row in matrix:
        if len_matrix != len(row):
            raise ValueError('Матрица не является квадратичной')
    for i in range(len_matrix):
        for j in range(len_matrix):
            if matrix[i][j] != matrix[j][i]:
                raise ValueError('Элементы матрицы симметричны относительно главной диагонали')
        if matrix[i][i] != 0:
            raise ValueError('Элемент матрицы на главной диагонали не равен 0')


def write_results(file_name, results, running_time):
    with open(file_name, 'w', encoding='utf8') as f:
        for index, element in enumerate(results):
            generation, value, individual = element
            individual = ' '.join([str(gen) for gen in individual])
            text = f"Результат №{index+1}\nПоколение: {generation}\nЗначение: {value}\nРаспределение: {individual}\n"
            f.write(text)
            f.write('\n')
        f.write(f"Время работы алгоритма: {running_time} минут(ы)")
