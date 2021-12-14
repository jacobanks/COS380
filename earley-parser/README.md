# Earley Parser

## Description
This parser takes a context free grammar (CFG) from a file and a sentence as input. With this it applies the earley parsing algorithm to the input sentence based on the CFG. It will output a parse tree either through NLTK or pretty_print. This parse tree will include each word in the sentence and its corresponding part of speech tag.

## Usage
To run the parser, simply run the following command:
```
python earleyparser.py sample-grammar.txt
```

Adding the 'draw' keyword as an argument uses NLTK to create a parse tree.
```
python earleyparser.py draw sample-grammar.txt
```

## Example Output with pretty_print:
```
      S              
      |               
      VP             
  ____|____           
 |         NP        
 |     ____|_____     
 |    |       Nominal
 |    |          |    
Verb Det        Noun 
 |    |          |    
book that      flight
```

```
                     S                                      
  ___________________|__________                            
 |      |                       VP                          
 |      |       ________________|_________________          
 |      |      |          NP                      PP        
 |      |      |      ____|_____           _______|_____    
 |      NP     |     |       Nominal      |             NP  
 |      |      |     |          |         |             |   
Aux  Pronoun  Verb  Det        Noun  Preposition      Proper
 |      |      |     |          |         |             |   
does    he   prefer that      flight   through       Indiana
```