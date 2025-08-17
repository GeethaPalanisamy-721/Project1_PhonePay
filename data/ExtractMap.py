# Extract map
import pandas as pd
import json
import os

""" Insurance Data """
def extract_insurance():
    path_mi= r"C:\Users\Siva Sankar\Desktop\Python Workspace\MDTM46B\PhonePay\data\map\insurance\hover\country\india\state"
    fm_insurance_list=os.listdir(path_mi)
    print(fm_insurance_list)

    clm={'State':[], 'Year':[],'Quarter':[],'District':[], 'Transaction_count':[], 'Transaction_amount':[]}

    for i in fm_insurance_list:
        p_i= os.path.join(path_mi,i)
        Map_yr=os.listdir(p_i)
        for j in Map_yr:
            p_j=os.path.join(p_i,j)
            Map_yr_list=os.listdir(p_j)
            for k in Map_yr_list:
                p_k=os.path.join(p_j,k)
                Data=open(p_k,'r')
                D=json.load(Data)
                for y in D['data']['hoverDataList']: # refer readme
                    Name=y['name']
                    count=y['metric'][0]['count']
                    amount=y['metric'][0]['amount']
                    clm['District'].append(Name)
                    clm['Transaction_count'].append(count)
                    clm['Transaction_amount'].append(amount)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quarter'].append(int(k.strip('.json')))
#Insurance DataFrame
    fm_insurance=pd.DataFrame(clm)

    fm_insurance["State"] = fm_insurance["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    fm_insurance["State"] = fm_insurance["State"].str.replace("-"," ")
    fm_insurance["State"] = fm_insurance["State"].str.title()
    fm_insurance['State'] = fm_insurance['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

    print("Map Insurance data Extracted ")
    print(fm_insurance.shape)
    return(fm_insurance)

""" Transaction data """
def extract_transaction():
    path_mt= r"C:\Users\Siva Sankar\Desktop\Python Workspace\MDTM46B\PhonePay\data\map\transaction\hover\country\india\state"
    fm_transaction_list=os.listdir(path_mt)
    #print(fm_transaction_list)

    clm={'State':[], 'Year':[],'Quarter':[],'District':[], 'Transaction_count':[], 'Transaction_amount':[]}

    for i in fm_transaction_list:
        p_i= os.path.join(path_mt,i)
        Map_yr=os.listdir(p_i)
        for j in Map_yr:
            p_j=os.path.join(p_i,j)
            Map_yr_list=os.listdir(p_j)
            for k in Map_yr_list:
                p_k=os.path.join(p_j,k)
                Data=open(p_k,'r')
                D=json.load(Data)
                for y in D['data']['hoverDataList']: # refer readme
                    Name=y['name']
                    count=y['metric'][0]['count']    # using index
                    amount=y['metric'][0]['amount']
                    clm['District'].append(Name)
                    clm['Transaction_count'].append(count)
                    clm['Transaction_amount'].append(amount)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quarter'].append(int(k.strip('.json')))
#Transaction DataFrame
    fm_transaction=pd.DataFrame(clm)

    fm_transaction["State"] = fm_transaction["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    fm_transaction["State"] =fm_transaction["State"].str.replace("-"," ")
    fm_transaction["State"] = fm_transaction["State"].str.title()
    fm_transaction['State'] = fm_transaction['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

    print("Map Transaction data Extracted ")
    print(fm_transaction.shape)
    return(fm_transaction)

""" User data """
def extract_user():
    path_mu= r"C:\Users\Siva Sankar\Desktop\Python Workspace\MDTM46B\PhonePay\data\map\user\hover\country\india\state"
    Map_user_list=os.listdir(path_mu)
    #print(Map_user_list)

    clm={'State':[], 'Year':[],'Quarter':[],'District':[], 'registeredUsers':[], 'appOpens':[]}

    for i in Map_user_list:
        p_i= os.path.join(path_mu,i)
        Map_yr=os.listdir(p_i)
        for j in Map_yr:
            p_j=os.path.join(p_i,j)
            Map_yr_list=os.listdir(p_j)
            for k in Map_yr_list:
                p_k=os.path.join(p_j,k)
                Data=open(p_k,'r')
                D=json.load(Data)
                for district,value in D["data"]["hoverData"].items(): #.items() to give key value pair in a loop
                                                                      #key: district, value: registeredusers and appopens
                    registereduser = value["registeredUsers"]
                    appopens = value["appOpens"]
                    clm["District"].append(district)
                    clm["registeredUsers"].append(registereduser)
                    clm["appOpens"].append(appopens)
                    clm["State"].append(i)
                    clm["Year"].append(j)
                    clm["Quarter"].append(int(k.strip(".json")))

#User DataFrame
    fm_user=pd.DataFrame(clm)

    fm_user["State"] = fm_user["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    fm_user["State"] = fm_user["State"].str.replace("-"," ")
    fm_user["State"] = fm_user["State"].str.title()
    fm_user['State'] = fm_user['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

    print("Map User data Extracted ")
    print(fm_user.shape)
    return(fm_user)

if __name__ == "__main__":
    fm_insurance = extract_insurance()
    fm_transaction = extract_transaction()
    fm_user = extract_user()

    fm_insurance.to_csv('insurance_map.csv',index=False)
    fm_transaction.to_csv('transaction_map.csv',index=False)
    fm_user.to_csv('user_map.csv',index=False)
    print("All datasets extracted and saved successfully")
    print(fm_insurance.columns)
    print(fm_transaction.columns)
    print(fm_user.columns)


