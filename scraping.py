from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

from utils import (concat_strings, get_file_name, get_str_group1,
                   get_str_group2, remove_repeated_from, run_manual_test,
                   write_to_json, write_to_txt)

sleep_time = int(input('Inform how many seconds the program should sleep: '))
test_time = 15

driver = webdriver.Chrome()

# First column of strings
group1 = get_str_group1()

# Second column of strings
group2 = get_str_group2()

# Concatenates both string columns to create a search query
search_strings = concat_strings(group1, group2)

dict = {} # will be used to store the data retrieved later

# Will wait for manual validation on google website
run_manual_test(driver, test_time)

links = [] # Stores all the links found

for str in search_strings:
    driver.get("https://scholar.google.com/")
    write_to_search_bar = driver.find_element(By.ID, "gs_hdr_tsi").send_keys(str)
    driver.find_element(By.ID, "gs_hdr_tsb").click() # Clicks search icon

    print(f'Retrieving results for "{str}"...')
    dict[str] = {} # Will store the results for a given str
    temp_links = []
    temp_titles = []
    result = driver.find_elements(By.CLASS_NAME, "gs_rt") # Store every result box

    # Stores every retrieved result in a particular list
    failed = 0
    for res in result:
        try:
            link = res.find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            failed = 1
            continue
        temp_links.append(link)
        temp_titles.append(res.text)
    if failed == 1:
        continue

    # Separately, stores every result in the dictionary
    i = 0
    for res in result:
        dict[str][i] = {}
        dict[str][i]["title"] = temp_titles[i]
        dict[str][i]["link"] = temp_links[i]
        i += 1
    for link in temp_links:
        links.append(link)

    # So that google does not detect automation
    if sleep_time > 0:
        sleep(sleep_time)

driver.quit()

json_name = get_file_name('.json')
print(f"Saving results to {json_name}...")
write_to_json(json_name, dict)

unique_links = remove_repeated_from(links)

txt_name = get_file_name('.txt')
print(f"Saving results to {txt_name}...")
write_to_txt(txt_name, dict, unique_links, search_strings)

print("Program terminated")

