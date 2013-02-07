main: main.o DPlot.o
	clang++ main.o DPlot.o -o main `root-config --libs`

main.o: main.cxx
	clang++ -c main.cxx -o main.o `root-config --cflags`

DPlot.o: DPlot.cxx
	clang++ -c DPlot.cxx -o DPlot.o `root-config --cflags`
