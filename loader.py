import yaml

class loader():
    def load_questions(file_path='data/questions.yml'):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        return data['questions']


    if __name__ == "__main__":
        questions = load_questions()
        for question in questions:
            print(f"Question: {question['question']}")
            for i, answer in enumerate(question['answers'], start=1):
                print(f"{i}. {answer}")