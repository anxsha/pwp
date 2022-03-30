import csv
with open('sains1.csv', 'r') as in_file, open('sains_removed_duplicates.csv', 'w') as out_file:
    reader = csv.DictReader(in_file)
    seen = set()
    out_file.write("cat,name,price\n")
    for row in reader:
        cat = str(row['\ufeffcat'])
        name = str(row['name'])
        price = str(row['price'])
        if name in seen:
            continue
        seen.add(name)
        name = name.replace(",", " ")
        cat = cat.replace(",", " &")
        if price[0] == "£":
            price = price.replace("£", "")
        elif price[-1] == "p":
            price = price.replace("p", "")
            price = f"{float(price)/100:.2f}"
        else:
            continue
        out_file.write(f'{cat},{name},{price}\n')
