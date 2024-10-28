from selenium import webdriver
import time, random
from selenium.webdriver.common.keys import Keys
driver = webdriver.Safari()
driver.maximize_window()
website = "https://wordly.org"
driver.get(website)
time.sleep(1)
#to get list of words
words = []
with open('words.txt', 'r') as words_file:
    words = [i[:-1] for i in words_file.readlines()] #Creating a list of 5-letter words

input_string = "adieu" #This is one of the most optimal starter strings as it contains maximum vowels
for attempt in range(1, 7):

    for i in range(1, 6):
        letter_box = '//*[@id="game-wrapper"]/div[1]/div[{0}]/div[{1}]'.format(attempt, i)
        driver.find_element("xpath", letter_box).send_keys(input_string[i - 1])#Enter letter in box

    time.sleep(2.75)
    # driver.find_element("xpath",'//*[@id="game-wrapper"]/div[6]/div[3]/div[9]').send_keys(Keys.ENTER)
    driver.find_element("xpath",'//*[@id="game-wrapper"]/div[6]/div[3]/div[9]').click()
    time.sleep(2.75)

    present_letters = []
    absent_letters = []
    correct_letters = []

    for i in range(1, 6):
        letter_box = '//*[@id="game-wrapper"]/div[1]/div[{0}]/div[{1}]'.format(attempt, i)
        box = driver.find_element("xpath", letter_box)
        box_color = box.value_of_css_property('background-color')

        if box_color == "rgb(164, 174, 196)":  #grey
            absent_letters.append(input_string[i - 1])
        elif box_color == "rgb(121, 184, 81)":  #green
            correct_letters.append([input_string[i - 1], i - 1])
        else:  #yellow
            present_letters.append([input_string[i - 1], i - 1])

    if len(correct_letters) == 5:  #If all letters are right, our word is found
        break

    temp_words = words[:]  #Creating a copy of words list to delete unnecessary words
    for letter in absent_letters:
        for word in words:
            if letter in word:
                try:
                    temp_words.remove(word)
                except:
                    continue
    for letter, index in present_letters:
        for word in words:
            try:
                if word[index] == letter or letter not in word:
                    temp_words.remove(word)
            except:
                continue
    for letter, index in correct_letters:
        for word in words:
            try:
                if word[index] != letter or letter not in word:
                    temp_words.remove(word)
            except:
                continue

    words = temp_words
    input_string = words[random.randint(0, len(words) - 1)] # choosing a random word from the remaining choices


