import json
import time

from selenium.webdriver.common.by import By


# momentaneous
def get_str_group1():
    group1 = [
        'Quantum computing',
        'Quantum computation',
        #'Indie developers',
        #'Brazilian game development',
        #'Indie game development',
        #'Brazilian indie games',
        #'Game development'
    ]
    return group1

# momentaneous
def get_str_group2():
    group2 = [
        'machine learning',
        'artificial intelligence',
        #'Difficulties',
        #'Obstacles',
        #'Support',
        #'Community',
        #'Acceleration'
    ]
    return group2


def treat_file_name(file_name, extension):
    if len(file_name) < 5:
        file_name += extension
    elif len(file_name) > 4 and file_name[-4:] != extension:
        file_name += extension
    return file_name


def concat_strings(group1, group2):
    concatenated_strings = []
    for str1 in group1:
        for str2 in group2:
            concatenated_strings.append(str1 + ' ' + str2)
    return concatenated_strings


def get_file_name(extension):
    json_name = ''
    while json_name == '':
        json_name = input(f"Inform the name of the {extension} file: ")
        json_name = treat_file_name(json_name, extension)
    return json_name


def write_to_txt(txt_name, dict, unique_links, search_strings):
    f = open(txt_name, "w")
    f.write(f'Total strings searched: {len(search_strings)}\n')
    f.write(f"Total unique links retrieved: {len(unique_links)}\n")

    for link in unique_links:
        f.write(f'{link}\n')

    f.write('='*100 + '\n')
    for search_string in dict.keys():
        f.write(search_string +'\n\n')
        for pair in dict[search_string].values():
            temp = tuple(pair.values()) # Converts returned values to a tuple, to write to file
            try:
                f.write(f'Title: {temp[0]}\n')
            except:
                f.write('Could not read title\n')
            f.write(f'Link: {temp[1]}\n\n')
        f.write('='*100 + '\n')

    f.close()


def write_to_json(json_name, dict):
    with open(json_name, 'w') as j:
        json.dump(dict, j, indent = 3)


def remove_repeated_from(links):
    unique = []
    for link in links:
        if link not in unique:
            unique.append(link)
    return unique


def run_manual_test(driver, test_time):
    driver.get("https://scholar.google.com/")
    driver.find_element(By.ID, "gs_hdr_tsi").send_keys('test')
    driver.find_element(By.ID, "gs_hdr_tsb").click() # Clicks search icon
    time.sleep(test_time)
