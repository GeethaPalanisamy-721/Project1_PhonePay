# Extract Aggregation
import pandas as pd
import json
import os

""" Insurance Aggregation """
def extract_insurance():
    path_ins= r"C:\Users\Siva Sankar\Desktop\Python Workspace\MDTM46B\PhonePay\data\aggregated\insurance\country\india\state"
    Agg_state_list=os.listdir(path_ins)
    # print(Agg_state_list)

    clm={'State':[], 'Year':[],'Quarter':[],'Transaction_type':[], 'Transaction_count':[], 'Transaction_amount':[]}

    for i in Agg_state_list:
        p_i= os.path.join(path_ins,i)
        Agg_yr=os.listdir(p_i)
        for j in Agg_yr:
            p_j=os.path.join(p_i,j)
            Agg_yr_list=os.listdir(p_j)
            for k in Agg_yr_list:
                p_k=os.path.join(p_j,k)
                Data=open(p_k,'r')
                D=json.load(Data)
                for z in D['data']['transactionData']:  #refer readme
                    Name=z['name']
                    count=z['paymentInstruments'][0]['count']   
                    amount=z['paymentInstruments'][0]['amount']
                    clm['Transaction_type'].append(Name)
                    clm['Transaction_count'].append(count)
                    clm['Transaction_amount'].append(amount)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quarter'].append(int(k.strip('.json')))
#Insurance DataFrame
    fd_insurance=pd.DataFrame(clm)
    
    fd_insurance["State"] = fd_insurance["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    fd_insurance["State"] = fd_insurance["State"].str.replace("-"," ")
    fd_insurance["State"] = fd_insurance["State"].str.title()
    fd_insurance['State'] = fd_insurance['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

    print("Insurance data Extracted")
    print(fd_insurance.shape)
    return(fd_insurance)

""" Transaction Aggregation """
def extract_transaction():
    path_trans = r"C:\Users\Siva Sankar\Desktop\Python Workspace\MDTM46B\PhonePay\data\aggregated\transaction\country\india\state"
    Agg_state_list = os.listdir(path_trans)
    # print(Agg_state_list)
    clm_trans = {'State':[], 'Year':[], 'Quarter':[], 'Transaction_type':[], 'Transaction_count':[], 'Transaction_amount':[]}

    for i in Agg_state_list:
        p_i = os.path.join(path_trans, i)
        Agg_yr = os.listdir(p_i)
        for j in Agg_yr:
            p_j = os.path.join(p_i, j)
            Agg_qtr = os.listdir(p_j)
            for k in Agg_qtr:
                p_k = os.path.join(p_j, k)
                with open(p_k, 'r') as Data:
                    D = json.load(Data)
                    for z in D['data']['transactionData']:
                        name = z['name']
                        count = z['paymentInstruments'][0]['count']
                        amount = z['paymentInstruments'][0]['amount']
                        clm_trans['Transaction_type'].append(name)
                        clm_trans['Transaction_count'].append(count)
                        clm_trans['Transaction_amount'].append(amount)
                        clm_trans['State'].append(i)
                        clm_trans['Year'].append(j)
                        clm_trans['Quarter'].append(int(k.strip('.json')))

# Convert to DataFrame
    fd_transaction = pd.DataFrame(clm_trans)

    fd_transaction["State"] = fd_transaction["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    fd_transaction["State"] = fd_transaction["State"].str.replace("-"," ")
    fd_transaction["State"] = fd_transaction["State"].str.title()
    fd_transaction['State'] = fd_transaction['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

    print("Transaction data Extracted")
    print(fd_transaction.shape)
    return fd_transaction

"""User Aggregation"""
def extract_user():
    path_user = r"C:\Users\Siva Sankar\Desktop\Python Workspace\MDTM46B\PhonePay\data\aggregated\user\country\india\state"
    Agg_state_list_user = os.listdir(path_user)
    #print("State in user data:", Agg_state_list_user)
    clm_user = {'State':[], 'Year':[], 'Quarter':[], 'Brand':[], 'Count':[], 'Percentage':[]}

    for i in Agg_state_list_user:
        p_i = os.path.join(path_user, i)
        Agg_yr = os.listdir(p_i)
        for j in Agg_yr:
            p_j = os.path.join(p_i, j)
            Agg_qtr = os.listdir(p_j)
            for k in Agg_qtr:
                p_k = os.path.join(p_j, k)
                with open(p_k, 'r') as Data:
                    D = json.load(Data)
                    users = D['data'].get('usersByDevice')
                    if users is not None:
                        for z in users:
                            brand = z['brand']
                            count = z['count']
                            perc = z['percentage']
                            clm_user['Brand'].append(brand)
                            clm_user['Count'].append(count)
                            clm_user['Percentage'].append(perc)
                            clm_user['State'].append(i)
                            clm_user['Year'].append(j)
                            clm_user['Quarter'].append(int(k.strip('.json')))
    fd_user = pd.DataFrame(clm_user)

    fd_user["State"] = fd_user["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
    fd_user["State"] = fd_user["State"].str.replace("-"," ")
    fd_user["State"] = fd_user["State"].str.title()
    fd_user['State'] = fd_user['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")
 
    print("User data Extracted")
    print(fd_user.shape)
    return fd_user

if __name__ == "__main__":
    fd_insurance = extract_insurance()
    fd_transaction = extract_transaction()
    fd_user = extract_user()

    fd_insurance.to_csv('insurance_aggr.csv',index=False)
    fd_transaction.to_csv('transaction_aggr.csv',index=False)
    fd_user.to_csv('user_aggr.csv',index=False)
    print("All datasets extracted and saved successfully")
    print(fd_user.columns)


