


Class = 'class' +className +'{' +classVarDec+'*'+  subroutineDec+'*'+ '}'

classVarDec = "(static | field) +"Type+ varName +"(, "+varName+")*"+ ';'

Type =  'int | char | boolean |' + className

subroutineDec =  ('constructor' | 'function' | 'method') ('void' | type) subroutineName
'(' parameterList ')' subroutineBody

parameterList: ( (type varName) (',' type varName)*)?

subroutineBody: '{' varDec* statements '}'


varDec: 'var' type varName (',' varName)* ';'


className: identifier


subroutineName: identifier


varName: identifier}