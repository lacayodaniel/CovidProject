from COV19Library import *
import random
import time
import matplotlib.pyplot as plt

def project_questions():
    # question 7
    lib = COV19Library()
    lib.LoadData("cov19_city.csv")
    # ensure all ids are unique by using a set (no duplicates)
    unique_ids = {lib.cityArray[-1].cid}
    # fill the set with 100 ids
    while len(unique_ids) <= 100:
        rand_pos = random.randint(0, lib.size-1)
        unique_ids.add(lib.cityArray[rand_pos].cid)
    # for i in lib.cityArray:
    #     unique_ids.add(i.cid)

    print("Linear search time:", end=" ")
    st = time.time()
    for id in unique_ids:
        lib.linearSearch(id, "id")
    # time spent on linear search should be around 0.0052
    lin_time = time.time() - st
    print(lin_time)

    print("BST built time:", end=" ")
    st = time.time()
    lib.buildBST()
    bst_build_time = time.time() - st
    # time spent building BST should be around 0.014
    print(bst_build_time)

    # question 8
    print("BST search time:", end=" ")
    st = time.time()
    for id in unique_ids:
        lib.searchBST(id)
    # time spent on BST search should be around 0.00027
    bst_search_time = time.time() - st
    print(bst_search_time)

    # question 9
    bst_time = bst_search_time + bst_build_time
    n = bst_build_time / (lin_time - bst_search_time)
    print("Ratio of total linear time to total BST time (build and search):", lin_time / bst_time)
    # on average the ratio is 1/4
    print("Approx.", ((bst_time - lin_time)*100/lin_time) + 100,
          "searches before total linear time is equal to total BST time")

    print(n)
    # on average it's approx. 300

    # question 10
    # plot daily increasing cases for city with the largest population
    max_pop = 0
    pop_city = None
    for city in lib.cityArray:  # find the city with the largest population
        if int(city.pop) > max_pop:
            max_pop = int(city.pop)
            pop_city = city
    print(pop_city)  # should be NY-NJ-PA with most population
    # daily increasing cases = (total cases on that day) - (total cases on the previous day)
    daily_inc = []
    for index in range(0, len(pop_city.cases) - 1):
        daily_inc.append(pop_city.cases[index + 1] - pop_city.cases[index])

    dates = lib.timeLine
    del dates[0]

    # plt.plot(dates, daily_inc)
    # plt.ylabel('Daily Increase in COVID-19 Cases')
    # plt.xlabel('Time (days)')
    # plt.xticks(rotation=90)
    # plt.show()


project_questions()

if __name__ == '__main__':
    lib = COV19Library()
    lib.LoadData("cov19_city.csv")
    print(lib.size) # should be 942
    print(lib.linearSearch("11940", "id")) # should be Athens
    print(lib.linearSearch("Winona", "name"))  # should be Winona
    #for each in lib.cityArray: print(each)
    print(lib.cityArray[-1]) # should be Angola
    print(lib.isSorted) # should be False
    lib.quickSort()
    print(lib.isSorted) # should be True
    print(lib.cityArray[-1])  # should be Zanesville
    lib.buildBST()
    print(lib.getHeight(lib.root)) # should be 12 or smaller
    print(lib.searchBST("34980")) # should be Nashville; Note there was no cstate in the spreadsheet
