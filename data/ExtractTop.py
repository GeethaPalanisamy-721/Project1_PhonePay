# Extract Top

import pandas as pd
import json
import os

""" Insurance Data """
def extract_insurance():
    path_ti= r"C:\Users\Siva Sankar\Desktop\Python Workspace\MDTM46B\PhonePay\data\top\insurance\country\india\state"
    ft_insurance_list=os.listdir(path_ti)
    print(ft_insurance_list)

    clm={'State':[], 'Year':[],'Quarter':[],'pincodes':[], 'Transaction_count':[], 'Transaction_amount':[]}

    for i in ft_insurance_list:
        p_i= os.path.join(path_ti,i)
        Map_yr=os.listdir(p_i)
        for j in Map_yr:
            p_j=os.path.join(p_i,j)
            Map_yr_list=os.listdir(p_j)
            for k in Map_yr_list:
                p_k=os.path.join(p_j,k)
                Data=open(p_k,'r')
                D=json.load(Data)
                
                for x in D['data']['pincodes']: # refer readme
                    entityName=x['entityName']
                    count=x['metric']['count']
                    amount=x['metric']['amount']
                    clm['pincodes'].append(entityName)
                    clm['Transaction_count'].append(count)
                    clm['Transaction_amount'].append(amount)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quarter'].append(int(k.strip('.json')))
#Insurance DataFrame
    ft_insurance=pd.DataFrame(clm)

    ft_insurance["State"] =ft_insurance["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    ft_insurance["State"] = ft_insurance["State"].str.replace("-"," ")
    ft_insurance["State"] = ft_insurance["State"].str.title()
    ft_insurance['State'] = ft_insurance['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

    print("Top Insurance data Extracted ")
    print(ft_insurance.shape)
    return(ft_insurance)

""" Transaction data """
def extract_transaction():
    path_tt= r"C:\Users\Siva Sankar\Desktop\Python Workspace\MDTM46B\PhonePay\data\top\transaction\country\india\state"
    ft_transaction_list=os.listdir(path_tt)
    #print(ft_transaction_list)

    clm={'State':[], 'Year':[],'Quarter':[],'pincodes':[], 'Transaction_count':[], 'Transaction_amount':[]}
    for i in ft_transaction_list:
        p_i= os.path.join(path_tt,i)
        Map_yr=os.listdir(p_i)
        for j in Map_yr:
            p_j=os.path.join(p_i,j)
            Map_yr_list=os.listdir(p_j)
            for k in Map_yr_list:
                p_k=os.path.join(p_j,k)
                Data=open(p_k,'r')
                D=json.load(Data)
                
                for x in D['data']['pincodes']: # refer readme
                    entityName=x['entityName']
                    count=x['metric']['count']
                    amount=x['metric']['amount']
                    clm['pincodes'].append(entityName)
                    clm['Transaction_count'].append(count)
                    clm['Transaction_amount'].append(amount)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quarter'].append(int(k.strip('.json')))
#Transaction DataFrame
    ft_transaction=pd.DataFrame(clm)

    ft_transaction["State"] = ft_transaction["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    ft_transaction["State"] = ft_transaction["State"].str.replace("-"," ")
    ft_transaction["State"] = ft_transaction["State"].str.title()
    ft_transaction['State'] = ft_transaction['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

    print("Top Transaction data Extracted ")
    print(ft_transaction.shape)
    return(ft_transaction)

""" User Data """
def extract_user():
    path_tu= r"C:\Users\Siva Sankar\Desktop\Python Workspace\MDTM46B\PhonePay\data\top\user\country\india\state"
    Top_user_list=os.listdir(path_tu)
    #print(Top_user_list)

    clm={'State':[], 'Year':[],'Quarter':[],'pincodes':[], 'registeredUsers':[]}
    for i in Top_user_list:
        p_i= os.path.join(path_tu,i)
        Map_yr=os.listdir(p_i)
        for j in Map_yr:
            p_j=os.path.join(p_i,j)
            Map_yr_list=os.listdir(p_j)
            for k in Map_yr_list:
                p_k=os.path.join(p_j,k)
                Data=open(p_k,'r')
                D=json.load(Data)
                
                for x in D['data']['pincodes']: # refer readme
                    name=x['name']
                    registeredUsers = x['registeredUsers']
                    clm['pincodes'].append(name)
                    clm['registeredUsers'].append(registeredUsers)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quarter'].append(int(k.strip('.json')))
#User DataFrame
    ft_user=pd.DataFrame(clm)

    ft_user["State"] = ft_user["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    ft_user["State"] = ft_user["State"].str.replace("-"," ")
    ft_user["State"] = ft_user["State"].str.title()
    ft_user['State'] = ft_user['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

    print("Top user data Extracted ")
    print(ft_user.shape)
    return(ft_user)

if __name__ == "__main__":
    ft_insurance = extract_insurance()
    ft_transaction = extract_transaction()
    ft_user = extract_user()

    ft_insurance.to_csv('insurance_top.csv',index=False)
    ft_transaction.to_csv('transaction_top.csv',index=False)
    ft_user.to_csv('user_top.csv',index=False)
    print("All datasets extracted and saved successfully")
    
    print(ft_insurance.columns)
    print(ft_transaction.columns)
    print(ft_user.columns)

