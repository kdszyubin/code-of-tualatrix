#include <stdlib.h>
#include <gtk/gtk.h>

int main( int   argc,
          char *argv[] )
{
    gint socket_id = 0;
    GtkWidget *window;
    GtkWidget *button;

    gtk_init (&argc, &argv);

    if(argc != 2)
    {
        g_message("usage: %s [socket]\n", argv[0]);

        return -1;
    } else {
        socket_id = atoi(argv[1]);
    }

    window = gtk_plug_new(socket_id);

    button = gtk_button_new ();

    gtk_widget_show (button);

    gtk_container_add (GTK_CONTAINER (window), button);

    gtk_widget_show (window);

    gtk_main ();

    return 0;
}
