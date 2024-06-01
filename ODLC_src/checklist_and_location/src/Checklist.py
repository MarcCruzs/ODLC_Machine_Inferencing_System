from ODLC_src.Classes.Predictors.PredictorCombiner import PredictorCombiner

class CheckList:
    def __init__(self, object: PredictorCombiner) -> None:
        self.__object_list = []
        self.__object = object
        self.__checklist = []

    def add_object(self, object: Any):
        self.__object_list.append(object)
        
    def remove_object(self, object: Any):
        self.__object_list.remove(object)

    def verify_object(self, object: Any) -> bool:
        if object in self.__object_list:
            self.remove_object(object)
            return True
        else:
            return False

    def load_checklist(self, filename: str) -> List[List[str]]:
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file.readlines()]

        self.__checklist = []
        temp = []

        for line in lines:
            if not line:
                continue  # Skip empty lines
            if len(temp) == 4:
                self.__checklist.append(temp)
                temp = []
            temp.append(line)

        if len(temp) == 4:
            self.__checklist.append(temp)

        return self.__checklist

def main():
    # Assuming you have a PredictorCombiner instance
    combiner = PredictorCombiner()
    checklist = CheckList(combiner)
    
    # Load the checklist from a file
    checklist_file = 'checklist.txt'
    multidimensional_array = checklist.load_checklist(checklist_file)
    
    # Print the multidimensional array
    for item in multidimensional_array:
        print(item)

if __name__ == "__main__":
    main()
