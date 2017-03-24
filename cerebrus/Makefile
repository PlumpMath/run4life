CC=g++
CFLAGS=-shared -fPIC
HDRS=cerebrus.h object.h logger.h world.h character.h navmesh.h node.h edge.h
OBJS=cerebrus.o object.o logger.o world.o character.o navmesh.o node.o edge.o
P3DINCL=-I/usr/include/panda3d -I/usr/include/python2.7 -I/usr/include/eigen3
P3DLIBS=-L/usr/lib/panda3d -lp3dtoolconfig -lpanda

%.o: %.cpp %.h
	$(CC) $(CFLAGS) $(P3DINCL) -c -o $@ $<

cerebrus_module.o: $(HDRS)
	interrogate $(P3DINCL) -S/usr/include/panda3d/parser-inc -Dvolatile -Dmutable -DCPPPARSER -D__STDC__=1 -D__cplusplus -D__inline -D__const=const -D__attribute__\(x\)= -D_LP64 -D_DEBUG -srcdir . -I. -oc libcerebrus_igate.cxx -od libcerebrus.in -fnames -string -refcount -assert -python-native -module cerebrus -library libcerebrus -promiscuous $(HDRS)
	interrogate_module -oc cerebrus_module.cxx -module cerebrus -library cerebrus -python-native libcerebrus.in
	$(CC) $(CFLAGS) -c $(P3DINCL) libcerebrus_igate.cxx
	$(CC) $(CFLAGS) $(P3DINCL) -c -o cerebrus_module.o cerebrus_module.cxx
	
pymod: cerebrus_module.o $(OBJS)
	$(CC) $(CFLAGS) $(P3DLIBS) -o cerebrus.so cerebrus_module.o libcerebrus_igate.o $(OBJS) /usr/lib/panda3d/libpanda.so /usr/lib/panda3d/libpanda.so /usr/lib/panda3d/libpandaexpress.so /usr/lib/panda3d/libp3dtool.so /usr/lib/panda3d/libp3dtoolconfig.so /usr/lib/python2.7/site-packages/panda3d/core.so

sharedlib: $(OBJS)
	$(CC) $(CFLAGS) -o libcerebrus.so $^

test: sharedlib test.h test.cpp
	$(CC) $(P3DINCL) -o test -L. -lcerebrus test.cpp

clean:
	rm -f *.o
	rm -f *.in
	rm -f *.cxx
