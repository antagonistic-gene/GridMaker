import quickstart
from quickstart import extract_doc_id_from_url, get_document_text, authenticate


def get_file(url):
    data = [[]]
    doc_id = extract_doc_id_from_url(url)
    #extracts doc id from url
    text = get_document_text(doc_id, authenticate())
    #using google api to receive content of document
    #print(text)
    data = set_coordinates(text, data)
    print_grid(data)

def set_coordinates(info, data):
    x, y, v = 0, 0, 0
    data2 = [[None for i in range(100000)] for j in range(100000)]
    d_t = 1
    start = False
    for i in info.split():
        if i == 'y-coordinate':
            #we can record data after this point in the table
            start = True
        elif i != ' ' and start == True and d_t == 1:
            x= int(i)
            d_t += 1
        elif i != ' ' and start == True and d_t == 2:
            v= i
            d_t += 1
        elif i != ' ' and start == True and d_t == 3:
            y = int(i)
            #print(x)
            #print(v)
            #print(y)
            data2[y][x] = v
            d_t -= 2
        else:
            continue
    return data2

def print_grid(data):
    for y in reversed(data):
        #we're traversing y coordinate backwards to print top down
        if y == ([None]* len(y)):
            #this will skip empty lines
            pass
        else:
            print("")
            #Adds new line each iteration
            for x in y:
                if x != None:
                    print(x, end = "")
                elif x == None:
                    print(" ", end="")

get_file("https://docs.google.com/document/d/1vyIXKsJYLf-2hoYfXwayRduSyk8ciCGY4kowG73TkYM/edit")