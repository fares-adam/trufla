#!/usr/bin/python3
import requests, json, typer, xmltodict , os , time
import pandas as pd
import pymongo
import urllib.parse

user_name = urllib.parse.quote_plus('trufla_admin')
pass_word = urllib.parse.quote_plus("p@ssw0rd")
client = pymongo.MongoClient(username="trufla_admin", password="p@ssw0rd")

mydb = client["trufla"]
#mydb.createUser( { "user": "trufla_admin", "pwd": "P@ssw0rd"})
collection1 = mydb["xml"]
collection2 = mydb["csv"]

# A function to call the API and enrich vehicle data for csv files


def enrich_csv(vehicles):
    # looping in vehicles list.
    for x in vehicles:
        # capturing parameters for API and calling it.
        vin = x["vin_number"]
        year = x["model_year"]
        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json&modelyear={year}"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        # capturing enriched  data and adding them to each vehicle inside list.
        p = json.loads(response.text)
        model = p["Results"][0]["Model"]
        manufacturer = p["Results"][0]["Manufacturer"]
        plant_country = p["Results"][0]["PlantCountry"]
        vehicle_type = p["Results"][0]["VehicleType"]
        x["model"] = model
        x["manufacturer"] = manufacturer
        x["plant_country"] = plant_country
        x["vehicle_type"] = vehicle_type
    return vehicles


# A function to call the API and enrich vehicle data for xml files.
def enrich_xml(vehicles: list):
    # looping in vehicles list.
    for x in vehicles:
        # capturing parameters for API and calling it.
        vin = x["VinNumber"]
        year = x["ModelYear"]
        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json&modelyear={year}"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        # capturing enriched  data and adding them to each vehicle inside list.
        p = json.loads(response.text)
        x["model"] = p["Results"][0]["Model"]
        x["manufacturer"] = p["Results"][0]["Manufacturer"]
        x["plant_country"] = p["Results"][0]["PlantCountry"]
        x["vehicle_type"] = p["Results"][0]["VehicleType"]
    return vehicles


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
    with open(f"/home/fares/Desktop/trufla/python_task_data/input_data/xml/{filename}.xml") as xml_file:
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
    print(json.dumps(final, indent=2, ensure_ascii=False))
    collection1.insert_one(final)


@app.command()
def csv(customer_file: str, vehicle_file: str):

    time_stamp = time.time()
    # reading csv  customer file to dataframe.
    csv_customer_file = pd.DataFrame(pd.read_csv(
        f"/home/fares/Desktop/trufla/python_task_data/input_data/csv/{customer_file}.csv", sep=",", header=0, index_col=False))
    # converting DataFrame to json and writing it to file for further use.
    csv_customer_file.to_json("csv_customer_file.json", orient="records", date_format="epoch",
                              double_precision=10, force_ascii=True, date_unit="ms", default_handler=None)
    # reading json data from file.
    f = open("csv_customer_file.json",)
    data = json.load(f)
    # removing tempfile
    os.remove("csv_customer_file.json")
    # reading csv  customer file to dataframe.
    csv_vehicles_file = pd.DataFrame(pd.read_csv(
        f"/home/fares/Desktop/trufla/python_task_data/input_data/csv/{vehicle_file}.csv", sep=",", header=0, index_col=False))
    # converting DataFrame to json and writing it to file for further use.
    csv_vehicles_file.to_json("csv_vehicles_file.json", orient="records", date_format="epoch",
                              double_precision=10, force_ascii=True, date_unit="ms", default_handler=None)
    # reading json data from file
    v = open("csv_vehicles_file.json",)
    vdata = json.load(v)
    trans_list = []
    # removing tempfile
    os.remove("csv_vehicles_file.json")
    # a function to return all transaction (bulk)

    def transaction():
        # looping through customer and vechiles and getting date ,and checking each vechile with customer and assign ownership
        for i in data:
            vehicles = []
            date = i.get("date")
            customer = i.copy()
            del customer["date"]
            for v in vdata:
                if customer["id"] == v["owner_id"]:
                    vehicles.append(v)
                    enrich_csv(vehicles)
                trans = {"date": date, "customer": customer,
                         "vehicles": vehicles}
                trans_list.append(trans)

    transaction()
    # looping through transaction list and removing duplicate dicts
    final_trans_list = [i for n, i in enumerate(
        trans_list) if i not in trans_list[n + 1:]]
    # completing final dict
    final = {"filename": f"{customer_file}_file1.csv_{vehicle_file}_file.csv",
             "transaction": final_trans_list}

    #print(json.dumps(final, indent=2, ensure_ascii=False))
    # inserting to db
    collection2.insert_one(final)


if __name__ == "__main__":
    app()
