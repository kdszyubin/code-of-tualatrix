CC = gcc

CFLAGS = -Wall -Wunused         \
    -DG_DISABLE_DEPRECATED      \
    -DGDK_DISABLE_DEPRECATED    \
    -DGDK_PIXBUF_DISABLE_DEPRECATED \
    -DGTK_DISABLE_DEPRECATED
 
all: plug socket

plug: plug.c
	$(CC) plug.c -o plug $(CFLAGS) `pkg-config gtk+-2.0 --cflags --libs`

socket: socket.c
	$(CC) socket.c -o socket $(CFLAGS) `pkg-config gtk+-2.0 --cflags --libs`

clean:
	rm -f *.o *
