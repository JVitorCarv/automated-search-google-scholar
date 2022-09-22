import json
from enum import unique
from re import search
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

sleep_time = int(input('Inform how many seconds the program should sleep: '))

driver = webdriver.Chrome()

# First column of strings
group1 = [
    'Indie game devs',
    'Independent game developer',
    'Indie developers',
    'Brazilian game development',
    'Indie game development',
    'Brazilian indie games',
    'Game development'
]

# Second column of strings
group2 = [
    'Incubator',
    'Challenges',
    'Difficulties',
    'Obstacles',
    'Support',
    'Community',
    'Acceleration'
]

# Concatenates both string columns to create a search query
search_strings = []
for str1 in group1:
    for str2 in group2:
        search_strings.append(str1 + ' ' + str2)

dict = {} # will be used to store the data retrieved later

search_strings.insert(0, "test")
driver.get("https://scholar.google.com/")
write_to_search_bar = driver.find_element(By.ID, "gs_hdr_tsi").send_keys(search_strings[0])
driver.find_element(By.ID, "gs_hdr_tsb").click() # Clicks search icon
search_strings.remove(search_strings[0])
sleep(20)

links = []

for str in search_strings:
    driver.get("https://scholar.google.com/")
    write_to_search_bar = driver.find_element(By.ID, "gs_hdr_tsi").send_keys(str)
    driver.find_element(By.ID, "gs_hdr_tsb").click() # Clicks search icon

    print(f'Retrieving results for "{str}"...')
    dict[str] = {} # Will store the results for a given str
    temp_links = []
    titles = []
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
        titles.append(res.text)
    if failed == 1:
        continue

    # Separately, stores every result in the dictionary
    i = 0
    for res in result:
        dict[str][i] = {}
        dict[str][i]["title"] = titles[i]
        dict[str][i]["link"] = temp_links[i]
        i += 1
    for link in temp_links:
        links.append(link)

    # So that google does not detect automation
    if sleep_time > 0:
        sleep(sleep_time)

driver.quit()

print("Saving results to results.json...")
j = open("results.json", "w")
json.dump(dict, j, indent = 3)
j.close()

for link in links:
    print(link)

unique_links = []
for link in links:
    if link not in unique_links:
        unique_links.append(link)

print("Saving results to results.txt...")
f = open("results.txt", "w")
f.write(f'Total strings searched: {len(search_strings)}\n')
f.write(f"Total unique links retrieved: {len(unique_links)}\n")

for link in unique_links:
    f.write(f'{link}\n')

f.write('='*100 + '\n')
for search_string in dict.keys():
    f.write(search_string +'\n\n')
    for pair in dict[search_string].values():
        # Converts returned values to a tuple, to write to file
        temp = tuple(pair.values())
        try:
            f.write(f'Title: {temp[0]}\n')
        except:
            f.write('Could not read title\n')
        f.write(f'Link: {temp[1]}\n\n')
    f.write('='*100 + '\n')

f.close()

print("Program terminated")

