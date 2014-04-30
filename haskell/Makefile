all: lexer.hs parser.hs
	ghc main.hs parser.hs lexer.hs types.hs -o clikeparser

lexer.hs: lexer.x
	alex lexer.x

lexer: lexer.hs
	ghc lexer.hs

parser.hs: parser.y
	happy parser.y

parser: lexer.hs types.hs parser.hs
	ghc types.hs lexer.hs parser.hs
