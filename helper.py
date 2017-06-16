from multiprocessing.dummy import Pool as ThreadPool
from html import get_html
import csv
import sys


def scrape(array, function, threads):
    # Define the number of threads
    pool = ThreadPool(threads)

    # Tell the user what is happening
    length = len(array)
    print(f"Scraping {length} items using {function} on {threads} threads.")

    # Calls get() and adds the filesize returned each call to an array called filesizes
    result = pool.map(function, array)
    pool.close()
    pool.join()
    return result


# Handle an error where data is not added to the end of the CSV file.
def add_new_line(file):
    # Add a newline to the end of the file if there is not one
    with open(file, "r+") as f:
        f.seek(0, 2)
        if(f.read() != '\n'):
            f.seek(0, 2)
            f.write('\n')


def tabulate(csvFile, array):
    # Files must be in the csv directory inside the project folder
    # Opens the CSV file
    with open("csv/%s.csv" % (csvFile), 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        # Adds a new line if there is not one present
        # add_new_line("csv/%s.csv" % (csvFile))
        # Add the array passed in to the CSV file
        for i in range(0, len(array)):
            if len(array[i]) > 0:
                writer.writerow(array[i])
    length = len(array)
    print(f"Succesfully tabulated {length} rows to {csvFile}.csv.")
    return True


def get_existing_data(csvFile, colNum):
    # Add the values in colNum in csvFile to an array
    array = []
    print(f"Reading data from {csvFile}.csv.")
    with open("csv/%s.csv" % (csvFile), encoding='utf-8') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            array.append(row[colNum])
    return array


def find_max(csvFile, colNum):
    # Find the maximum value in a column in an array
    array = []
    print(f"Reading data from {csvFile}.csv.")
    with open("csv/%s.csv" % (csvFile), encoding='utf-8') as csvfile:
        next(csvfile)
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            array.append(int(row[colNum]))
    return max(array)


def remove_existing_data(existing, new):
    # Remove data we already have from the list of new data to parse
    for i in new[:]:
        if i in existing:
            new.remove(i)
    # Convert new values to a set to remove duplicates, then back to a list
    new = list(set(new))
    length = len(new)
    print(f"{length} new items to add.")
    return new


def un_dimension(array, item):
    # Pulls specific items from an multi-dimensional array and returns them to one array
    result = []
    for i in range(0, len(array)):
        result.append(array[i][item])
    return result


def fix_array(array, value):
    # Used to clean match info results for matches with more than one map
    for i in range(0, len(array)):
        if len(array[i]) < value:
            for b in range(0, len(array[i])):
                array.append(array[i][b])
            array.remove(array[i])
    return array


def fix_player_stats(array):
    # Used to clean match info results for matches with more than one map
    newArray = []
    for i in range(0, len(array)):
        for b in range(0, len(array[i])):
            newArray.append(array[i][b])
    return newArray


def get_new_iterable_items(page, startID):
    # Iterate through unique IDs until we get the last one, then return them to a list
    print(f"Checking for new {page}s. This may take awhile.")
    check = True
    array = []
    while check:
        startID += 1
        html = get_html(f"https://www.hltv.org/{page}/{startID}/a")
        if html is None:
            check = False
        else:
            sys.stdout.write('\r'+"New %s found: %s" % (page, startID))
            sys.stdout.flush()
            array.append(startID)
    length = len(array)
    print(f"\nFound {length} new {page}s.")
    return array
