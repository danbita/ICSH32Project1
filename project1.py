from pathlib import Path

def check_valid_starter_input(input_str: list[str]) -> bool:
    '''ensures that initial input is valid, containing either a R or D
    followed by a valid directory. 
    '''
    if len(input_str) < 2:
        print('ERROR')
        return False
    elif input_str[0] != 'D' and input_str[0] != 'R':
        print('ERROR')
        return False
    elif not Path(input_str[1]).exists():
        print('ERROR')
        return False
    return True

def check_valid_later_input(input_str: list[str]) -> bool:
    '''ensures that initial input is valid, containing either a valid command
    followed by a valid directory. 
    '''
    valid_commands = ['A', 'N', 'E', 'T', '<', '>']
    if input_str[0] == 'A':
        return True
    if len(input_str) < 2:
        print('ERROR')
        return False
    elif not input_str[0] in valid_commands:
        print('ERROR')
        return False
    elif input_str[0] in ['<', '>'] and not input_str[1].isnumeric():
        print('ERROR')
        return False
    return True

def read_input(beginning: bool) -> list[str]:
    '''reads whatever input the user enters, splits line into a command
    and into whatever information is needed for that file. boolean beginning 
    value refers to whether this is one the initial commamds (R or D)
    or one of the later commands
    '''
    input_str = input().split()
    if beginning:
        while(not check_valid_starter_input(input_str)):
            input_str = input().split()
    else:
        while(not check_valid_later_input(input_str)):
            input_str = input().split()
    return input_str

def read_final_input() -> str:
    'Reads the final action item that happens to the intersting files'
    input_str = input()
    while not input_str in ['F', 'D', 'T']:
        print("ERROR")
        input_str = input()
    return input_str

def lexigraphical_sort(l: list[str]) -> list[str]:
    'lexigraphically sorts list, first by file depth and then lexigraphic order'
    sorted(l, key = lambda file: len(file.parts))
    cur_depth = len(l[0].parts)
    last_index = 0
    for i in range(1, len(l)):
        if len(l[i].parts) > cur_depth:
            l[last_index : i] = sorted(l[last_index : i])
            cur_depth = len(l[i].parts)
            last_index = i
    l[last_index: ] = sorted(l[last_index: ])
    return l

def lexigraphical_print(l: list[str]) -> list[str]:
    'prints a list in lexigraphical order'
    l = lexigraphical_sort(l)
    for element in l:
        print(element)
    return l
 
def process_initial_input(input_str: list[str]) -> list[str]:
    'processes the intial input command'
    p = Path(input_str[1])
    sorted_paths = []
    if input_str[0] == 'D':
        for element in p.iterdir():
            if element.is_file():
                sorted_paths.append(element)
    elif input_str[0] == 'R':
          for element in p.iterdir():
              if element.is_file():
                  sorted_paths.append(element)
              elif element.is_dir():
                  sorted_paths.extend(process_initial_input(['R', element]))
    return sorted(sorted_paths, key = lambda file: len(file.parts))
    

def find_specific_files(eligible_files: list[str], file_name: str) -> list[str]:
    'Find specific files in a directory (step "N")'
    sorted_list = []
    for file in eligible_files:
        if Path(file).name == file_name:
            sorted_list.append(file)
    return lexigraphical_print(sorted_list)

def find_specific_extensions(eligible_files: list[str], extension: str) -> list[str]:
    'Find specific extensions in a directory (step "E")'
    sorted_list = []
    if extension[0] != '.':
        extension = '.' + extension
    for file in eligible_files:
        if Path(file).suffix == extension:
            sorted_list.append(file)
    return lexigraphical_print(sorted_list)

def file_contains_text(file: Path, text) -> bool:
    'Checks if a file contains certain text'
    f = open(file, 'r')
    text_list = f.readlines()
    f.close()
    for substr in text_list:
        if substr == text or text in substr:
            return True
    return False

def find_specific_text(eligible_files: list[str], text: str) -> list[str]:
    'Find files with specific text in a directory (step "E")'
    sorted_list = []
    for file in eligible_files:
        if file.name == '.DS_Store':
            continue
        if file_contains_text(Path(file), text):  
            sorted_list.append(file)
    return lexigraphical_print(sorted_list)

def find_smaller_files(eligible_files: list[str], size: int) -> list[str]:
    'find files smaller than a certain size'
    sorted_list = []
    for file in eligible_files:
        if Path(file).stat().st_size < size:
            sorted_list.append(file)
    return lexigraphical_print(sorted_list)

def find_larger_files(eligible_files: list[str], size: int) -> list[str]:
    'find files larger than a certain size'
    sorted_list = []
    for file in eligible_files:
        if Path(file).stat().st_size > size:
            sorted_list.append(file)
    return lexigraphical_print(sorted_list)
    
def process_new_inputs(input_str: list[str], eligible_files: list[str]) -> list[str]:
    'processes later input commands regarding eligible files'
    if input_str[0] == 'A':
        return lexigraphical_print(eligible_files)
    elif input_str[0] == 'N':
        return find_specific_files(eligible_files, input_str[1])
    elif input_str[0] == 'E':
        return find_specific_extensions(eligible_files, input_str[1])
    elif input_str[0] == 'T':
        return find_specific_text(eligible_files, input_str[1])
    elif input_str[0] == '<':
        return find_smaller_files(eligible_files, int(input_str[1]))
    elif input_str[0] == '>':
        return find_larger_files(eligible_files, int(input_str[1]))

def print_first_line(file: Path):
    'prints the first line of a file'
    if not file.suffix in ['.txt', '.csv', '.json', '.xml', '.html', '.py', '.java', '.c', '.cpp', '.js', '.md', '.log']:
        print("NOT TEXT")
        return
    f = file.open('r')
    print(f.readline().rstrip('\n'))
    f.close()
    
def duplicate_file(file):
    'duplicates a file'
    Path(file.as_posix() + '.dup').touch()

def process_action(action: str, file: str):
    'processes the final action that will apply to the interesting files'
    if action == 'F':
        print_first_line(Path(file))
    elif action == 'D':
        duplicate_file(file)
    elif action == 'T':
        Path(file).touch()
    

def run():
    'runs the script'
    user_input = read_input(True)
    eligible_files = process_initial_input(user_input)
    lexigraphical_print(eligible_files)
    sorting_method = read_input(False)
    interesting_list = process_new_inputs(sorting_method, eligible_files)    
    action = read_final_input()
    for file in interesting_list:
        process_action(action, file)
    
    
if __name__ == '__main__':
    run()
    
