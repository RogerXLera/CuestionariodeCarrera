"""
Roger Lera
2023/06/19
"""
import os
import pandas as pd
import numpy as np
import csv
from definitions import * # classes Skill, Activity, TimePeriod, TimePeriodSequence, Job, User Preference, Topics
import json


def read_jobs(file_path,sheet_name='Specialist tasks'):
    """
        This function reads the file containing the jobs  
    """
    df = pd.read_excel(file_path,sheet_name=sheet_name) #store file in pandas.DataFrame

    current_job_name = str(df.iloc[0]['ANZSCO Title'])
    current_skills = []
    jobs = []
    for i in range(len(df)):
        line_ = df.iloc[i] #df line
        name_ = str(line_['ANZSCO Title'])
        if current_job_name != name_:
            for s in current_skills:
                j.skills.append(s)
            jobs.append(j)
            current_job_name = name_
            current_skills = []

        
        id_ = line_['ANZSCO Code']
        j = Job(id=id_,name=name_,descriptor='') #create job object
        skill_ = line_['Specialist Task']
        presence = line_[f'% of time spent on task']
        cluster = line_['Specialist Cluster']
        family = line_['Cluster Family']
        s = Skill(skill_,1,presence,cluster=cluster,family=family)
        current_skills.append(s)
        
    for s in current_skills:
        j.skills.append(s)
    jobs.append(j)
    
    return jobs


def read_jobs_a(file_path,sheet_name='Table 5',trigger_="Skill Level"):
    """
        This function reads the file containing the jobs  
    """
    mgroups = [str(i) for i in range(1,9)]
    df = pd.read_excel(file_path,sheet_name=sheet_name) #store file in pandas.DataFrame
    cols = df.columns
    copy_job = False
    J = {}
    for i in range(len(df)):
        row = df.iloc[i]
        if copy_job:
            for j in range(len(cols)):
                cell = str(row[cols[j]])
                if cell[0] in mgroups:
                    id = cell
                    name = row[cols[j+1]]
                    J.update({id:Job(id=id,name=name)})
                    break
        else:
            for j in range(len(cols)):
                cell = row[cols[j]]
                if cell == trigger_:
                    copy_job = True


    
    return J


def read_questions(file_path):
    # Open and read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
    Q = {}
    for qd in data['decisions']:
        q = Question(qd['id'],"")
        if 'text' in qd.keys():
            q.question = qd['text']
        if 'true' in qd.keys():
            q.predecesor += qd['true']
        Q.update({q.id:q})

    return Q

def read_questions_dict():
    
    filename = 'data/questions_dict.json'
    filepath = os.path.join(os.getcwd(),filename)
    f = open(filepath)
    dict_ = json.load(f)
    new_dict = {int(k):v for k,v in dict_.items()}
    f.close()

    return new_dict

def read_jobs_dict():
    
    filename = 'data/anzsco_job_dict.json'
    filepath = os.path.join(os.getcwd(),filename)
    f = open(filepath)
    dict_ = json.load(f)
    f.close()

    return dict_
    

if __name__ == '__main__':

    wd_ = 'data'
    file_ = "anzsco.xlsx"
    file_path = os.path.join(os.getcwd(),wd_,file_)

    levels = ["Major Group",
              "Sub-Major Group",
              "Minor Group",
              "Unit Group",
              "Occupation"]
    J = read_jobs_a(file_path)

    file_ = "questions.json"
    file_path = os.path.join(os.getcwd(),wd_,file_)
    Q = read_questions(file_path)
    for q in Q.keys():
        print(type(q))
        print(Q[q])
        print(Q[q].predecesor)

    for j in J.keys():
        print(type(j))
        break


    q_dict = read_questions_dict()
    j_dict = read_jobs_dict()