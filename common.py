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
            for i in range(len(items)):

                if items[i].startswith('Вопрос'):
                    question = ' '.join(items[i].split('\n')[1:])
                    questions.append(question)
                    answer = ' '.join(items[i + 1].split('\n')[1:])
                    answers.append(answer)

    return dict(zip(questions, answers))
