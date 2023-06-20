"""
Roger Lera
2023/01/07
"""
import os
import pandas as pd
import numpy as np
import csv

class Skill:
    """
    This class stores the information about skills and its level.
    """

    def __init__(self,name,level,presence=0.5,probability=0.5,cluster=None,family=None):
        self.name = name
        self.level = level
        self.presence = presence
        self.probability = probability
        self.cluster = cluster
        self.family = family


    def __str__(self):
        string_ = f"Skill: {self.name} \t Level: {self.level}"
        return string_

    def check_skill(self,skill_list):
        """
            This function checks if a given skill is in a list and returns the skill
            and its level or the self skill and level 0 if it is not found
        """
        for s in skill_list:
            if s.name == self.name: #skill found in list returning level
                return s,s.level
        
        return self,0 # skill not found, returning level 0
    
    def add_skill(self,skill_list):
        """
            This function adds a given skill in a list and updates it's level if it is higher
        """
        s,lev_ = self.check_skill(skill_list)
        if lev_ == 0: #skill not found
            skill_list.append(self)
        else: #skill found, check level and update
            if self.level > s.level: #update
                skill_list.remove(s)
                skill_list.append(self)
                 

class Job:
    """
    This class stores the information about Jobs and its methods.
    """

    def __init__(self,id,name,descriptor=None):
        self.id = id
        self.name = name
        self.skills = [] #skills needed for obtaining the job

    def __str__(self):
        string_ = f"Job: {self.name} ({self.id})"
        return string_
    
    def __repr__(self):
        return self.id
    
    def ancestor(self,J,n_group):
        
        id_ = self.id[:n_group]
        return J[id_]


class Question:
    
    def __init__(self,id,question):
        self.id = id
        self.question = question
        self.predecesor = [] #questions following the question

    def __str__(self):
        return f"Q{self.id}: {self.question}"
    
    def __repr__(self):
        return str(self.id)