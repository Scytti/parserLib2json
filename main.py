# После парсинга имеем следующую структуру:
# "Название ячейки": {
#   input:[
#       "вход",
#       ...
#   ]
#   output: {
#       "выход" : "логическая функция",
#       ...
#   }
# }
import json
from liberty.parser import parse_liberty

pathToLibrary = "/home/daniil/workdir/synth/Example/sky130_fd_sc_hd__ff_100C_1v65.lib"
pathToFile = "/home/daniil/workdir/synth/Example/lib.json"

def read_information_from_library(path_to_library):
    library = parse_liberty(open(path_to_library).read())

    input_pins = []
    output_pins = {}
    cell_library = {}

    for cell_group in library.get_groups('cell'):
        cell_name = (str(cell_group.args[0]))[1:len(str(cell_group.args[0])) - 1]
        for pin_group in cell_group.get_groups('pin'):
            pin_name_attribute = str(pin_group.args[0])[1:len(str(pin_group.args[0])) - 1]
            pin_direction_attribute = pin_group['direction']
            if pin_direction_attribute == "output":
                pin_function_attribute = str(pin_group["function"])[1:len(str(pin_group["function"])) - 1]
                output_pins[pin_name_attribute] = pin_function_attribute
            else:
                input_pins.append(pin_name_attribute)
        cell_library[cell_name] = {'input': input_pins, 'output': output_pins, }

        input_pins = []
        output_pins = {}

    return cell_library

def write_to_json(cells, path_to_file):
    with open(path_to_file, 'w') as outfile:
        json.dump(cells, outfile, sort_keys=True, indent=4)

write_to_json(read_information_from_library(pathToLibrary), pathToFile)

