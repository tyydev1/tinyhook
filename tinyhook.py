import json

def read_db():
    with open('data/installed.json', 'r') as file:
        return json.load(file)
    

if __name__ == '__main__':
    data = read_db()
    print(data)