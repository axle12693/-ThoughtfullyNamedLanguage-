INCLUDES= /opt/homebrew/Cellar/ossp-uuid/1.6.2_2/include/
LIBPATH= /opt/homebrew/Cellar/ossp-uuid/1.6.2_2/lib


main: main.cpp lexer.cpp parse.cpp generate.cpp
	clang++ -std=c++20 main.cpp -o main -I $(INCLUDES) -L $(LIBPATH) -luuid

large: main.cpp lexer.cpp parse.cpp generate.cpp
	make main
	time ./main ../largefile.tnl
	./main file.tnl
	