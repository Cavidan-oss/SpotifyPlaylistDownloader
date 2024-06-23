import os
class File_Handler(object):

    def __init__(self):
        pass

    def write_to_txt(self, data, filename,mode='w',path = ''):

        try:
            with open(filename, mode, encoding="utf-8") as file:
                file.write('\n'.join(data))
            return "Sucessfull Attempt"
        except:
            raise Exception("Something went wrong!")


    def write_to_json(self, data, filename, mode ='w', path = '', indent = 4):
        try:
            with open(filename, mode) as file:
                json.dump(data, file, indentation = indent)
            return "Sucessfull Attempt"
        except:
            raise Exception("Something went wrong!")

    def read_txt(self, filename):
        with open(filename, 'r', encoding="utf-8") as file:
            data = file.read().split('\n')

        return data

    def read_json(self, filename, encoding="utf-8"):
        import json
        
        with open(filename, 'r') as file:
            data = json.load(filename)

        return data

    def change_dir_to(self,path):

        if os.path.exists(os.path.join(os.getcwd(), path)):

            os.chdir(path)
            return True

        return False

    def create_folder(self, folder_name, mode = 0o666):

        
        path = os.path.join(os.getcwd(), folder_name)
        os.mkdir(path, mode)
        print(path)
        if os.path.exists(folder_name):
            return True

        return False

          


