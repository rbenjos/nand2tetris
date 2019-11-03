PROGRAM_STRUCTURE= {'class': 'class'+className+'{'+classVarDec+'*'+subroutineDec'*'+'}',
classVarDec: ('static' | 'field' ) type varName (',' varName)* ';'
type: 'int' | 'char' | 'boolean' | className
subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) subroutineName
 '(' parameterList ')' subroutineBody
parameterList: ( (type varName) (',' type varName)*)?
subroutineBody: '{' varDec* statements '}'
varDec: 'var' type varName (',' varName)* ';'
className: identifier
subroutineName: identifier
varName: identifier}