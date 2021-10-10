#!/usr/bin/python3
import json, typer, xmltodict , os , time
import pandas as pd



# typer module for CLI.
app = typer.Typer()
# XML cli
# make sure to ask about if the user needs to give the extension with the file name or not
# example : parser.py xml file1.xml


@app.command()
def xml(filename: str):
    time_stamp = time.time()
    # open the input xml file and read
    # data in form of python dictionary
    # using xmltodict module
    with open(f"/home/fares/Desktop/trufla/python_task_data/input_data/xml/{time_stamp}_{filename}.xml") as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
        xml_file.close()
        # generate the object using json.dumps() , changing from orderedDict to normal dict.
        # corresponding to json data
        json_data = json.dumps(data_dict)
    # gettinig data to use individually
    s = json.loads(json_data)
    insurance = s.get("Insurance")
    transaction = insurance.get("Transaction")
    tt = transaction.copy()
    date = transaction.get("Date")
    customer = transaction.get("Customer")
    id = customer.get("@id")
    name = customer.get("Name")
    add = customer.get("Address")
    phone = customer.get("Phone")
    units = customer.get("Units")
    if units:
        auto = units.get("Auto")
        # wrapping vehicles dict(s) in a list
        # using a temp variable to ensure order not changed
        vehicles_temp = list(auto.values())
        vehicles = []
        # changing @id key to id .
        for i in vehicles_temp:
            print(i)
            if isinstance(i, dict):
                i = {"id" if k == "@id" else k: v for k, v in i.items()}
                vehicles.append(i)
            elif isinstance(i,list):
                for x in i:
                    print(x , "x")
                    x={"id" if k == "@id" else k: v for k, v in x.items()}
                    print(x , "x after")
                    vehicles.append(x)

            #vehicles.append(i)
    else:
        vehicles = []
    # putting customer dict into proper format
    customer = {"id": id, "name": name, "address": add, "phone": phone}
    # putting the transaction dict into proper format and inserting customer dict
    trans = {"date": date, "customer": customer, "vehicles": vehicles}

    # merging all dicts into the final dict
    final = {"filename": f"{filename}.xml", "transacrtion": [trans]}
    # Write the json data to db
    # json file
    with open(f"/home/fares/Desktop/trufla/python_task_data/output/xml/{time_stamp}_{filename}.json", "w") as json_file:
        json_file.write(json.dumps(final, indent=2, ensure_ascii=False))
        json_file.close()
        print(json.dumps(final, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    app()
