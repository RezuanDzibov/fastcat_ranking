import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

fields = ['entry_id', 'year', 'breed', 'rank', 'dog_name', 'gender', 'speed']


def get_breed_names(driver):
    list_of_breed_name = []
    for breed in driver.find_element(By.ID, 'in_cde_bvg_num').find_elements(By.TAG_NAME, 'option'):
        list_of_breed_name.append(breed.text.strip())
    return list_of_breed_name[1:]


def get_years(driver):
    list_of_year = []
    for year in driver.find_element(By.NAME, 'in_year').find_elements(By.TAG_NAME, 'option'):
        list_of_year.append(year.text.strip())
    return list_of_year[:-1]


def get_dog_parameters(dog_row):
    dog_row_parameters = []
    for dog_row_parameter in dog_row.find_elements(By.TAG_NAME, 'td'):
        dog_row_parameters.append(dog_row_parameter.text.strip())
    return dog_row_parameters


def select_year(driver, year_index):
    year_select = Select(driver.find_element(By.NAME, 'in_year'))
    year_select.select_by_index(year_index)


def select_breed(driver, breed_index):
    breed_select = Select(driver.find_element(By.ID, 'in_cde_bvg_num'))
    breed_select.select_by_index(breed_index)


def click_search_button(driver):
    driver.find_element(By.NAME, 'showdogs').click()


def get_dog_rows(driver):
    dog_row_table = driver.find_element(By.CLASS_NAME, 'etrTable')
    dog_row_list = dog_row_table.find_elements(By.TAG_NAME, 'tr')
    return dog_row_list[1:]


def get_dog_parameter_dict(dog_row, entry_id, year, breed_name):
    dog_parameter_list = get_dog_parameters(dog_row=dog_row)
    dog_parameter_rows = fields[3:]
    dog_parameter_dict = {'entry_id': entry_id, 'year': year, 'breed': breed_name}
    for dog_parameter_index, dog_parameter in enumerate(dog_parameter_list):
        dog_parameter_dict[f'{dog_parameter_rows[dog_parameter_index]}'] = dog_parameter
    return dog_parameter_dict


def main(csv_file_name='dogs.csv'):
    print("Let's start!")
    with webdriver.Chrome() as driver:
        entry_id = 1
        driver.get('https://www.apps.akc.org/apps/fastcat_ranking/')
        list_of_breed_name = get_breed_names(driver=driver)
        list_of_year = get_years(driver=driver)
        with open(csv_file_name, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fields)
            writer.writeheader()
            for breed_index, breed_name in zip(range(1, len(list_of_breed_name)), list_of_breed_name):
                for year_index, year in zip(range(len(list_of_breed_name) + 1), list_of_year):
                    select_year(driver=driver, year_index=year_index)
                    select_breed(driver=driver, breed_index=breed_index)
                    click_search_button(driver=driver)
                    try:
                        dog_row_list = get_dog_rows(driver=driver)
                        for dog_row in dog_row_list:
                            dog_parameter_dict = get_dog_parameter_dict(
                                dog_row=dog_row,
                                entry_id=entry_id,
                                year=year,
                                breed_name=breed_name
                            )
                            print(dog_parameter_dict)
                            writer.writerow(dog_parameter_dict)
                            entry_id += 1
                    except NoSuchElementException:
                        continue


if __name__ == '__main__':
    print('Start!')
    csv_filename = input('Would you like to input csv file name? (example: filename.csv or just filename) or just push Enter >>> ')
    try:
        if csv_filename:
            if csv_filename.endswith('.csv'):
                main(csv_file_name=csv_filename)
            else:
                main(csv_file_name=f'{csv_filename}.csv')
        else:
            main()
    except KeyboardInterrupt:
        print("You've stopped the script.")