import os


def get_questions():
    questions = []
    answers = []

    path = 'quiz-questions'
    questions_files = [file for file in os.listdir(path)]

    for questions_file in questions_files:
        current_path = os.path.join(path, questions_file)

        with open(current_path, 'r', encoding='KOI8-R') as file:
            items = file.read().split('\n\n')
            for item in items:

                if item.startswith('Вопрос'):
                    question = ' '.join(item.split('\n')[1:])
                    questions.append(question)
                if item.startswith('Ответ'):
                    answer = ' '.join(item.split('\n')[1:])
                    answers.append(answer)

    return dict(zip(questions, answers))

