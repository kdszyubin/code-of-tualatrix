C=gcc
all:
	$(CC) `pkg-config --cflags --libs gtk+-2.0 gconf-2.0 gnome-vfs-2.0` -I/usr/include/firefox/gtkembedmoz -I/usr/include/firefox -I/usr/include/firefox/xpcom -I/usr/include/firefox/string -I/usr/include/firefox/nspr  -Wl,-rpath -Wl,/usr/lib/firefox -L/usr/lib/firefox -lgtkembedmoz -lxpcom -lplds4 -lplc4 -lnspr4 -ldl -lc -lpthread  pagico.c -o pagico
