#!/usr/bin/env python
#-*- coding:UTF-8 -*-
#########################################################################
# File Name: parse_rule_file.py
# Author: NLP_zhaozhenyu
# Mail: zhaozhenyu_tx@126.com
# Created Time: 14:33:27 2020-06-18
#########################################################################
import sys
import re
from ahocorapy.keywordtree import KeywordTree

class rule_parser:
    def __init__(self,concept_path = './concept.txt',rule_path='./rule.txt'):
        #read custom concept
        self.concept_words = self.parse_concept_file(concept_path)
        ##get atomic rule name that is INCOUT and BEFORE as ["INCOUT_c_school_1","BEFORE_c_school_c_man"]
        self.atomic_op = set()
        #read custom rules 
        self.rules = self.parse_rules(rule_path)
        self.valid_operation = {'(':0,'IN_':-1,'BEFORE_':-1,'AND':3,'OR':2,')':0}
        self.init_context()


    def parse_concept_file(self,path):
        '''
        input: concept file path
        output:diction ,e.g.{"c_school":set('school','college')}
        '''
        concept = {}
        for lines in open(path):
            data = lines.strip().split(':',1)
            #check
            if len(data)!=2:
                raise SystemExit('concept defined wrong: '+lines.strip())
            name = data[0].strip()
            if name in concept:
                raise SystemExit(word+' can not been defined twice!')
            if not name.startswith('c_'):
                raise SystemExit('concept must start with c_ ')
            

            cur = set()
            for word in data[1].split(','):
                word = word.strip()
                #rm extra blank space
                if len(word)==0:
                    continue
                if word.startswith('c_'):
                    try:
                        cur = set.union(cur,concept[word])
                    except:
                        raise SystemExit(word+' has not been defined')
                else:

                    cur.add(word)
            concept[name] = cur
        return concept

    def parse_rules(self,path):
        '''
        input: input file
        output: diction where key is rulename,value is operation or concept list
        e.g. {'r_1':['IN_c_school','AND','IN_c_man']}
        '''
        rules = {}
        #check and regular
        for lines in open(path):
            data = lines.strip().split(':',1)
            #check
            
            if len(data)!=2:
                raise SystemExit('rule defined wrong: '+lines.strip())
            name = data[0].strip()
            if name in rules:
                raise SystemExit(word+' can not been defined twice!')
            if not name.startswith('r_'):
                raise SystemExit('rule must start with r_ ')
            cur = ['(']
            for item in data[1].split(' '):
                if len(item)>0:
                    if item.startswith('r_'):
                        try:
                            cur.extend(rules[item])
                        except:
                            raise SystemExit(item+' has not been defined')
                    else:
                        cur.append(item)
                        if item.startswith('IN_') or item.startswith('BEFORE_'):
                            self.atomic_op.add(item)
            cur.append(')')
            rules[name] = cur
        return rules
    
    def init_context(self):
        concept_context = {}
        for k in self.atomic_op:
            if k.startswith('IN_'):
                concept = '_'.join(k.split('_')[1:-1])
                kt = KeywordTree(case_insensitive=False)
                for keyword in self.concept_words[concept]:
                    kt.add(keyword)
                kt.finalize()
                concept_context[k] = kt
            else:
                #BEFORE
                pass
        self.concept_context = concept_context


    def get_atomic_res(self,doc):
        res = {}
        for k in self.concept_context:
            res[k] = False
            if k.startswith('IN_'):
                num = int(k.split('_')[-1])
                cur = self.concept_context[k].search_all(doc)
                if cur !=None:
                    cur_num = 0
                    for i in cur:
                        cur_num +=1
                    if cur_num >= num:
                        res[k] = True
                        
            else:
                #BEFORE
                pass
        return res
    def match(self,doc):
        self.atomic_res = self.get_atomic_res(doc)
        res = {}
        for rule in self.rules:
            res[rule] = self.calculate(rule,doc)
        return res
    def calculate(self,rule,doc):
        res_list = []
        op_list = ['(']
        cur = 1
        while(len(op_list)>0):
            if cur==len(self.rules[rule]):
                break
            item = self.rules[rule][cur]
            if item.startswith('IN_') or item.startswith('BEFORE_')<0:
                res_list.append(self.atomic_res[item])
                cur += 1
            else:
                last = op_list.pop()
                while(self.valid_operation[item] <= self.valid_operation[last]):
                    if item == ')' and last == '(' :
                        break
                    elif item == '(':
                        break
                    else:
                        
                        if last == 'OR':
                            a = res_list.pop()
                            b = res_list.pop()
                            res_list.append(a or b)
                            last = op_list.pop()
                        elif last == 'AND':
                            a = res_list.pop()
                            b = res_list.pop()
                            res_list.append(a and b)
                            last = op_list.pop()
                        else:
                            raise SystemExit(last+' has not been defined!')
                if item == ')' and last == '(' :
                    pass
                else:
                    op_list.append(last)
                    op_list.append(item)
                cur +=1
        return res_list.pop()






if __name__ == '__main__':
    sports_rule = rule_parser('./sports_college/concept.txt','./sports_college/rule.txt')
    print(sports_rule.match('Jame  is a boy and study at junier high school, boy'))
