# OVERVIEW : A RULE SYSTEM
    A rule system for matching keywords and rules in text document. 
    You can define concepts and rules recursively.
    The Rules include three part: concepts ,operators and rules
### 1.concept: 
    keywords or concepts
        e.g.
        c_woman:  woman , women, wife
        c_girl: girl
        c_female: c_woman, c_girl
    
        you need write concepts like c_<concept name> : [concept1] ,[concept2],... in concept.txt
    
### 2.operators:
    
    1. IN_<concept>_<num> : 
    e.g.  IN_c_woman_3 means weather the document has at least three keywords in c_woman concept,return true or false
    
    2. AND : e.g.
    IN_c_woman_3 AND IN_c_girl_1 means document has at least three keywords in c_woman and has at least one girl word
    
    3. OR : 
    used like "or" in python
    
### 3.rules:
    r_<rule name> : [operator}|rule]:
    e.g. 
    r_1:IN_c_woman_3
    r_2: IN_c_girl_1 AND  r_1 OR  IN_c_female_1 
    you can write rules like Expressions with "()" in rule.txt

# USAGE:
    1. make dir like example of sports_college
    
    2. write rules in rule.txt and concept in concept.txt
    
    3. python parse_rule_file or write you own parser in main.py
