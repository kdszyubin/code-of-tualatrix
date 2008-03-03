#include <gtk/gtk.h>
#include <gconf/gconf-client.h>
#include <gtkembedmoz/gtkmozembed.h>
#include <libgnomevfs/gnome-vfs.h>
#include <libgnomevfs/gnome-vfs-utils.h>
#include <libgnomevfs/gnome-vfs-application-registry.h>
#include <gdk/gdk.h>
#include <gdk/gdkkeysyms.h>
#include <glib/gi18n.h>


#define	ICON	"/usr/share/pixmaps/pagico.png"
#define	MANUAL	"/opt/pagico/UserManual.pdf"

static 	gchar	*default_browser;

typedef struct _PagicoClient{
	GtkWidget *window;	
	GtkWidget *vbox;

	GtkAccelGroup *group;
	
	GtkWidget *menubar;
	GtkWidget *navigation_item;
	GtkWidget *navigation_menu;
	GtkWidget *new_item;
	GtkWidget *new_menu;
	GtkWidget *topic;
	GtkWidget *contact;
	GtkWidget *dashboard;
	GtkWidget *notes;
	GtkWidget *data;
	GtkWidget *relations;
	GtkWidget *separatormenuitem;
	GtkWidget *preferences;
	GtkWidget *lock;
	GtkWidget *help_item;
	GtkWidget *help_menu;
	GtkWidget *website;
	GtkWidget *release;
	GtkWidget *manual;
	GtkWidget *about;

	GtkWidget *mozembed;
}PagicoClient;

GList *browser_list;
static int num_browsers=0;

static PagicoClient *pagico_client_new(guint32 chromeMask);

static void	manual_item_activate_cb 	(GtkWidget *widget,PagicoClient *browser);

static void	about_item_activate_cb		(GtkWidget *widget,PagicoClient *browser);

static void	webiste_menu_item_activate_cb	(GtkWidget *widget,PagicoClient *browser);

static void	release_menu_item_activate_cb	(GtkWidget *widget,PagicoClient *browser);

static void	contact_menu_item_activate_cb	(GtkWidget *widget,PagicoClient *browser);

static void	topic_menu_item_activate_cb	(GtkWidget *widget,PagicoClient *browser);

static void	lock_menu_item_activate_cb	(GtkWidget *widget,PagicoClient *browser);

static void	dashboard_menu_item_activate_cb	(GtkWidget *widget,PagicoClient *browser);

static void	notes_menu_item_activate_cb	(GtkWidget *widget,PagicoClient *browser);

static void	data_menu_item_activate_cb	(GtkWidget *widget,PagicoClient *browser);

static void	relations_menu_item_activate_cb	(GtkWidget *widget,PagicoClient *browser);

static void	preferences_menu_item_activate_cb	(GtkWidget *widget,PagicoClient *browser);

static void	uri_item_activate_cb		(GtkWidget *widget,gchar *uri,PagicoClient *browser);

static void 	title_changed_cb		(GtkMozEmbed *embed,PagicoClient *browser);

static void 	new_window_cb			(GtkMozEmbed *embed,
						GtkMozEmbed **retval,guint chromemask,
						PagicoClient *browser);

static void 	destroy_cb			(GtkWidget *widget,PagicoClient *browser);

static void 	destroy_brsr_cb			(GtkMozEmbed *embed,PagicoClient *browser);

static gboolean	delete_cb			(GtkWidget *widget,GdkEventAny *event,
						PagicoClient *browser);
static int	open_uri_cb			(GtkMozEmbed *embed,const char *uri,
						PagicoClient *browser);

static void	location_changed_cb		(GtkMozEmbed *embed, PagicoClient *browser);

static void	link_message_cb			(GtkMozEmbed *embed, PagicoClient *browser);

static void	load_started_cb			(GtkMozEmbed *embed, PagicoClient *browser);

static void	net_state_change_all_cb		(GtkMozEmbed *embed, const char *uri,
				     		guint32 flags, guint status,
				    		PagicoClient *browser);

static gboolean button_pressed			(GtkWidget *eventbox,
						GdkEventButton *event,
						GtkWidget *widget);

static void	getcurrentsize			(GtkWidget *widget,PagicoClient *browser);

int main(int argc,char *argv[])
{
	gchar *fullpath;
	GConfClient *client;

	gtk_set_locale();
	gtk_init(&argc,&argv);

	client=gconf_client_get_default();
	default_browser = gconf_client_get_string(client,"/desktop/gnome/applications/browser/exec",NULL);

	fullpath=g_build_filename(g_get_home_dir(),".pagico",NULL);
	gtk_moz_embed_set_profile_path(fullpath,"browser");

	PagicoClient *browser=pagico_client_new(GTK_MOZ_EMBED_FLAG_DEFAULTCHROME);

	g_free(fullpath);

	gtk_main();

	return 0;
}

static PagicoClient *pagico_client_new(guint32 chromeMask)
{
	guint32 actualChromeMask=chromeMask;
	PagicoClient *browser=0;

	num_browsers++;

	browser=g_new0(PagicoClient,1);

	browser_list=g_list_prepend(browser_list,browser);

	g_message("New Pagico Window Created.\n");

	if(chromeMask==GTK_MOZ_EMBED_FLAG_DEFAULTCHROME)
	{
		actualChromeMask=GTK_MOZ_EMBED_FLAG_ALLCHROME;
	}

	gtk_window_set_default_icon_from_file(ICON,NULL);
	
	browser->window=gtk_window_new(GTK_WINDOW_TOPLEVEL);

	gtk_window_set_default_size(GTK_WINDOW(browser->window),1024,700);

	gtk_window_set_title(GTK_WINDOW(browser->window),"Pagico");
	gtk_window_set_position(GTK_WINDOW(browser->window),GTK_WIN_POS_CENTER_ALWAYS);
	
	browser->vbox=gtk_vbox_new(FALSE,0);
	gtk_container_add(GTK_CONTAINER(browser->window),browser->vbox);
	g_signal_connect(G_OBJECT(browser->window),"delete_event",GTK_SIGNAL_FUNC(delete_cb),browser);

/*创建菜单，但是只为第一个窗体创建*/
	if(num_browsers==1){
		browser->menubar = gtk_menu_bar_new();
		gtk_widget_show (browser->menubar);
		gtk_box_pack_start(GTK_BOX(browser->vbox),browser->menubar,FALSE,FALSE,0);
		gtk_widget_set_events (browser->menubar, GDK_POINTER_MOTION_MASK | GDK_POINTER_MOTION_HINT_MASK | GDK_BUTTON_PRESS_MASK | GDK_BUTTON_RELEASE_MASK);

		browser->group = gtk_accel_group_new();
		gtk_window_add_accel_group(GTK_WINDOW(browser->window),browser->group);

		browser->navigation_item = gtk_menu_item_new_with_mnemonic (_("_Navigation"));
		gtk_widget_show (browser->navigation_item);
		gtk_container_add (GTK_CONTAINER (browser->menubar), browser->navigation_item);

		browser->navigation_menu = gtk_menu_new ();
		gtk_menu_item_set_submenu (GTK_MENU_ITEM (browser->navigation_item), browser->navigation_menu);
		gtk_menu_set_accel_group(GTK_MENU(browser->navigation_menu),browser->group);
		gtk_widget_set_events (browser->navigation_menu, GDK_POINTER_MOTION_MASK | GDK_POINTER_MOTION_HINT_MASK | GDK_BUTTON_PRESS_MASK | GDK_BUTTON_RELEASE_MASK);

		browser->new_item = gtk_menu_item_new_with_mnemonic (_("_New"));
		gtk_widget_show (browser->new_item);
		gtk_container_add (GTK_CONTAINER (browser->navigation_menu), browser->new_item);

		browser->new_menu = gtk_menu_new ();
		gtk_menu_item_set_submenu (GTK_MENU_ITEM (browser->new_item), browser->new_menu);
		gtk_widget_set_events (browser->new_menu, GDK_POINTER_MOTION_MASK | GDK_POINTER_MOTION_HINT_MASK | GDK_BUTTON_PRESS_MASK | GDK_BUTTON_RELEASE_MASK);

		browser->topic = gtk_menu_item_new_with_mnemonic (_("_Topic"));
		gtk_widget_show (browser->topic);
		gtk_container_add (GTK_CONTAINER (browser->new_menu), browser->topic);

		browser->contact = gtk_menu_item_new_with_mnemonic (_("_Contact"));
		gtk_widget_show (browser->contact);
		gtk_container_add (GTK_CONTAINER (browser->new_menu), browser->contact);

		browser->dashboard = gtk_menu_item_new_with_mnemonic (_("_Dashboard"));
		gtk_widget_show (browser->dashboard);
		gtk_container_add (GTK_CONTAINER (browser->navigation_menu), browser->dashboard);

		browser->notes = gtk_menu_item_new_with_mnemonic (_("N_otes"));
		gtk_widget_show (browser->notes);
		gtk_container_add (GTK_CONTAINER (browser->navigation_menu), browser->notes);

		browser->data = gtk_menu_item_new_with_mnemonic (_("D_ata"));
		gtk_widget_show (browser->data);
		gtk_container_add (GTK_CONTAINER (browser->navigation_menu), browser->data);

		browser->relations = gtk_menu_item_new_with_mnemonic (_("_Relations"));
		gtk_widget_show (browser->relations);
		gtk_container_add (GTK_CONTAINER (browser->navigation_menu), browser->relations);

		browser->separatormenuitem = gtk_separator_menu_item_new ();
		gtk_widget_show (browser->separatormenuitem);
		gtk_container_add (GTK_CONTAINER (browser->navigation_menu), browser->separatormenuitem);
		gtk_widget_set_sensitive (browser->separatormenuitem, FALSE);

		browser->preferences = gtk_menu_item_new_with_mnemonic (_("_Preferences"));
		gtk_widget_show (browser->preferences);
		gtk_container_add (GTK_CONTAINER (browser->navigation_menu), browser->preferences);

		browser->separatormenuitem = gtk_separator_menu_item_new ();
		gtk_widget_show (browser->separatormenuitem);
		gtk_container_add (GTK_CONTAINER (browser->navigation_menu), browser->separatormenuitem);
		gtk_widget_set_sensitive (browser->separatormenuitem, FALSE);

		browser->lock = gtk_menu_item_new_with_mnemonic (_("_Lock Pagico"));
		gtk_widget_show (browser->lock);
		gtk_container_add (GTK_CONTAINER (browser->navigation_menu), browser->lock);

		browser->help_item = gtk_menu_item_new_with_mnemonic (_("_Help"));
		gtk_widget_show (browser->help_item);
		gtk_container_add (GTK_CONTAINER (browser->menubar), browser->help_item);

		browser->help_menu = gtk_menu_new ();
		gtk_menu_item_set_submenu (GTK_MENU_ITEM (browser->help_item), browser->help_menu);
		gtk_widget_set_events (browser->help_menu, GDK_POINTER_MOTION_MASK | GDK_POINTER_MOTION_HINT_MASK | GDK_BUTTON_PRESS_MASK | GDK_BUTTON_RELEASE_MASK);

		browser->website = gtk_menu_item_new_with_mnemonic (_("_Pagico Website"));
		g_signal_connect(G_OBJECT(browser->website),"activate",G_CALLBACK(webiste_menu_item_activate_cb),browser);
		gtk_widget_show (browser->website);
		gtk_container_add (GTK_CONTAINER (browser->help_menu), browser->website);

		browser->release = gtk_menu_item_new_with_mnemonic (_("_Release Note"));
		gtk_widget_show (browser->release);
		gtk_container_add (GTK_CONTAINER (browser->help_menu), browser->release);

		browser->manual = gtk_menu_item_new_with_mnemonic (_("_User Manual"));
		g_signal_connect(G_OBJECT(browser->manual),"activate",G_CALLBACK(manual_item_activate_cb),NULL);
		gtk_widget_show (browser->manual);
		gtk_container_add (GTK_CONTAINER (browser->help_menu), browser->manual);

		browser->separatormenuitem = gtk_separator_menu_item_new ();
		gtk_widget_show (browser->separatormenuitem);
		gtk_container_add (GTK_CONTAINER (browser->help_menu), browser->separatormenuitem);
		gtk_widget_set_sensitive (browser->separatormenuitem, FALSE);

		browser->about = gtk_menu_item_new_with_mnemonic (_("_About Pagico"));
		gtk_widget_show (browser->about);
		gtk_container_add (GTK_CONTAINER (browser->help_menu), browser->about);

/*创建快捷键*/
		gtk_widget_add_accelerator(browser->topic,"activate",browser->group,GDK_T,GDK_CONTROL_MASK,GTK_ACCEL_VISIBLE);
		g_signal_connect(G_OBJECT(browser->topic),"activate",G_CALLBACK(topic_menu_item_activate_cb),browser);

		gtk_widget_add_accelerator(browser->contact,"activate",browser->group,GDK_R,GDK_CONTROL_MASK,GTK_ACCEL_VISIBLE);
		g_signal_connect(G_OBJECT(browser->contact),"activate",G_CALLBACK(contact_menu_item_activate_cb),browser);

		gtk_widget_add_accelerator(browser->dashboard,"activate",browser->group,GDK_1,GDK_CONTROL_MASK,GTK_ACCEL_VISIBLE);
		g_signal_connect(G_OBJECT(browser->dashboard),"activate",G_CALLBACK(dashboard_menu_item_activate_cb),browser);

		gtk_widget_add_accelerator(browser->notes,"activate",browser->group,GDK_2,GDK_CONTROL_MASK,GTK_ACCEL_VISIBLE);
		g_signal_connect(G_OBJECT(browser->notes),"activate",G_CALLBACK(notes_menu_item_activate_cb),browser);

		gtk_widget_add_accelerator(browser->data,"activate",browser->group,GDK_3,GDK_CONTROL_MASK,GTK_ACCEL_VISIBLE);
		g_signal_connect(G_OBJECT(browser->data),"activate",G_CALLBACK(data_menu_item_activate_cb),browser);

		gtk_widget_add_accelerator(browser->relations,"activate",browser->group,GDK_4,GDK_CONTROL_MASK,GTK_ACCEL_VISIBLE);
		g_signal_connect(G_OBJECT(browser->relations),"activate",G_CALLBACK(relations_menu_item_activate_cb),browser);

		g_signal_connect(G_OBJECT(browser->preferences),"activate",G_CALLBACK(preferences_menu_item_activate_cb),browser);

		gtk_widget_add_accelerator(browser->lock,"activate",browser->group,GDK_L,GDK_CONTROL_MASK,GTK_ACCEL_VISIBLE);
		g_signal_connect(G_OBJECT(browser->lock),"activate",G_CALLBACK(lock_menu_item_activate_cb),browser);

		g_signal_connect(G_OBJECT(browser->about),"activate",G_CALLBACK(about_item_activate_cb),NULL);

		g_signal_connect(G_OBJECT(browser->release),"activate",G_CALLBACK(release_menu_item_activate_cb),browser);
	}

	browser->mozembed=gtk_moz_embed_new();
	gtk_box_pack_start(GTK_BOX(browser->vbox),browser->mozembed,TRUE,TRUE,0);
	gtk_moz_embed_load_url(GTK_MOZ_EMBED(browser->mozembed),"http://127.0.0.1:1200/?nopopup");

/*
 *下面全部是触发的相关信号
 *
 */

/*改变标题时触发的信号
	g_signal_connect(G_OBJECT(browser->mozembed),"title",
			GTK_SIGNAL_FUNC(title_changed_cb),browser);
*/

/*指到链接时得出当前链接
	g_signal_connect(G_OBJECT(browser->mozembed),"link_message",
			GTK_SIGNAL_FUNC(link_message_cb),browser);
*/

//请求建立新窗口时触发的信号
	g_signal_connect(G_OBJECT(browser->mozembed),"new_window",
			GTK_SIGNAL_FUNC(new_window_cb),browser);
//请求摧毁当前窗口时触发的信号
	g_signal_connect(G_OBJECT(browser->mozembed),"destroy_browser",
			GTK_SIGNAL_FUNC(destroy_brsr_cb),browser);
//当窗口被摧毁时触发的信号
	g_signal_connect(G_OBJECT(browser->mozembed),"destroy",
			G_CALLBACK(destroy_cb),browser);
//当有URL事件时的信号
	gtk_signal_connect(GTK_OBJECT(browser->mozembed), "open_uri",
			GTK_SIGNAL_FUNC(open_uri_cb),browser);

//当有位置改变时触发的信号
	gtk_signal_connect(GTK_OBJECT(browser->mozembed), "location",
			GTK_SIGNAL_FUNC(location_changed_cb),browser);
/*当开始访问网络时触发的信号*/
	gtk_signal_connect(GTK_OBJECT(browser->mozembed), "net_start",
			GTK_SIGNAL_FUNC(load_started_cb), browser);
/*所有网络活动的信号*/
	gtk_signal_connect(GTK_OBJECT(browser->mozembed), "net_state_all",
			GTK_SIGNAL_FUNC(net_state_change_all_cb), browser);


	gtk_widget_show_all(browser->window);

	return browser;
}

void load_started_cb	(GtkMozEmbed *embed, PagicoClient *browser)
{
	g_message("Load link to: %s",gtk_moz_embed_get_location(embed));
	
}

void link_message_cb	(GtkMozEmbed *embed, PagicoClient *browser)
{
	g_message("The link is: %s",gtk_moz_embed_get_link_message(embed));
	
}

void net_state_change_all_cb (GtkMozEmbed *embed, const char *uri,
				     guint32 flags, guint status,
				     PagicoClient *browser)
{
//&&flags==65537
//&&flags==786448
	if(uri){
		g_message("net_state_change_all_cb %s %u %d\n", uri, flags, status);
		if(flags==65537 || flags==65552){
			if(g_str_has_prefix(uri,"http://pagico.local/")){
				gtk_moz_embed_stop_load(embed);

				g_message("Catch the open file signal");
				
				const GnomeVFSURI *fileuri;
				GnomeVFSMimeApplication *app;

				gnome_vfs_init();
				
				fileuri=gnome_vfs_uri_new(uri);

				const gchar *filepath=gnome_vfs_uri_get_path(fileuri);

				g_print("the file is %s\n",filepath);

				const gchar *mime_type=gnome_vfs_get_mime_type_for_name(filepath);
				g_print("mime type of the file is %s\n",mime_type);

				app=gnome_vfs_mime_get_default_application(mime_type);
				if(app!=NULL){
					const gchar *binary_name=gnome_vfs_mime_application_get_binary_name(app);
					g_print("the file need %s and %s to open it\n",app->name,binary_name);
							
					gchar *shell=g_strconcat(binary_name," ",filepath,NULL);
					g_spawn_command_line_async(shell,NULL);

					g_free(shell);
				}
				
				gnome_vfs_mime_application_free (app);
				/*
	 			g_free(shell);
				g_free(mime_type);
				g_free(filepath);
				*/
			}
			else if(g_str_has_prefix(uri,"http://127.0.0.1:1200/temp/")||g_str_has_prefix(uri,"http://127.0.0.1:1200/html/iSpace/Exported.zip")){
				g_message("Catch the Save file signal");
				gtk_moz_embed_stop_load(embed);

				GnomeVFSURI *fileuri;

				gnome_vfs_init();
				
				fileuri=gnome_vfs_uri_new(uri);

				const gchar *filepath=gnome_vfs_uri_get_path(fileuri);
				g_print("the file is %s\n",filepath);


				GtkWidget *dialog;
				dialog = gtk_file_chooser_dialog_new ("Save file to...",GTK_WINDOW(browser->window),
								      GTK_FILE_CHOOSER_ACTION_SAVE,
								      GTK_STOCK_CANCEL, GTK_RESPONSE_CANCEL,
								      GTK_STOCK_SAVE, GTK_RESPONSE_ACCEPT,
									NULL);
				gtk_file_chooser_set_do_overwrite_confirmation (GTK_FILE_CHOOSER (dialog), TRUE);

				const gchar *filename;
				filename=g_basename(filepath);

				gtk_file_chooser_set_current_folder (GTK_FILE_CHOOSER (dialog), g_get_home_dir());
				gtk_file_chooser_set_current_name (GTK_FILE_CHOOSER (dialog), filename);

				if (gtk_dialog_run (GTK_DIALOG (dialog)) == GTK_RESPONSE_ACCEPT)
				{
					gchar *tempname = gtk_file_chooser_get_filename (GTK_FILE_CHOOSER (dialog));
					g_message(tempname);

					gchar *shell=g_strconcat("cp ","/opt/pagico",filepath," ",tempname,NULL);
					g_spawn_command_line_sync(shell,
								NULL,
								NULL,
								NULL,
								NULL);

					g_free (tempname);
				}

				gtk_widget_destroy (dialog);
			}
		}
		else if(flags==786448){
			if(g_str_has_prefix(uri,"http://127.0.0.1:1200/html/iSpace/SlideShow.php")){
				g_message("Open SlideShow");

				gtk_window_maximize(GTK_WINDOW(browser->window));
			}
		}
	}
}

void destroy_brsr_cb(GtkMozEmbed *embed,PagicoClient *browser)
{
	g_message("destroy_brsr_cb\n");
	gtk_widget_destroy(browser->window);
}

void new_window_cb(GtkMozEmbed *embed,GtkMozEmbed **newembed,guint chromemask,PagicoClient *browser)
{
	g_message("new_window_cb");
	g_print("embed is %p chromemask is %d\n",(void *)embed,chromemask);

	gchar *url;
	
	url=gtk_moz_embed_get_link_message(embed);
	g_print("THE LOAD URL IS %s\n",url);

	if(g_str_has_prefix(url,"http://")&&!g_str_has_prefix(url,"http://127.0.0.1:1200")){
		GError *error;
		gsize uri_size;
		gchar *shell;
		GString *uri_withsharp,*uri_clean;
		
		shell=g_strconcat(default_browser," ",url,NULL);

		uri_withsharp=g_string_new(shell);

		uri_size=uri_withsharp->len-2;

		uri_clean=g_string_new_len(shell,uri_size);

		g_spawn_command_line_async(uri_clean->str,NULL);

		g_free(shell);
		g_string_free(uri_withsharp,TRUE);
		g_string_free(uri_clean,TRUE);
	}else{
		PagicoClient *newbrowser=pagico_client_new(chromemask);
		*newembed=GTK_MOZ_EMBED(newbrowser->mozembed);
		g_print("new browser is \n%p\n",(void *)*newembed);
	}
	g_free(url);
}

void title_changed_cb(GtkMozEmbed *embed,PagicoClient *browser)
{
	gchar *newtitle;
	g_message("title_changed_cb");

	newtitle=gtk_moz_embed_get_title(embed);

	if(newtitle)
	{
		gtk_window_set_title(GTK_WINDOW(browser->window),newtitle);
		g_free(newtitle);
	}
}

void location_changed_cb (GtkMozEmbed *embed, PagicoClient *browser)
{
	gchar *newlocation;
	g_message("location_changed_cb");

	newlocation=gtk_moz_embed_get_location(embed);

	if(newlocation)
	{
		g_print("location change to %s\n\n",newlocation);
		g_free(newlocation);
	}
}

gint open_uri_cb(GtkMozEmbed *embed, const char *uri, PagicoClient *browser)
{
	g_message("Open URI: %s", uri);

	if(uri!=NULL && !g_str_has_prefix(uri,"javascript") && !g_str_has_prefix(uri,"about:blank")){
		GnomeVFSURI *full_uri;
		gnome_vfs_init ();

		full_uri=gnome_vfs_uri_new(uri);
		g_print("Resolved URI is: %s\n\n",gnome_vfs_uri_to_string(full_uri,GNOME_VFS_URI_HIDE_NONE));
		if(gnome_vfs_uri_is_local(full_uri)){
/*			GtkWidget *popup;
			GtkWidget *probar;

			popup=gtk_window_new(GTK_WINDOW_TOPLEVEL);
			gtk_window_set_default_size(GTK_WINDOW(popup),400,100);
			gtk_window_set_title(GTK_WINDOW(popup),"Now Loading");
			gtk_widget_show(popup);

			probar=gtk_progress_bar_new();
			gtk_progress_set_percentage(probar,0.8);
			gtk_progress_bar_set_text(probar,"Progress");
			gtk_widget_show(probar);
			gtk_container_add(GTK_CONTAINER(popup),probar);

			const gchar *path=gnome_vfs_uri_get_path(full_uri);
			g_print("要拖的文件是:%s\n",path);
*/

			gchar *filepath=g_filename_from_uri(uri,NULL,NULL);
			g_print("解析后的文件名是:%s\n",filepath);
			gchar *shell=g_strconcat("cp \"",filepath,"\" /opt/pagico/temp/dragged",NULL);
			g_spawn_command_line_sync(shell,NULL,NULL,NULL,NULL);
			gtk_moz_embed_load_url(GTK_MOZ_EMBED(browser->mozembed),"http://127.0.0.1:1200/html/iSpace/GetImported.php");
			g_free(filepath);

			return TRUE;
		}
		else if(g_str_has_prefix(uri,"http://")&&!g_str_has_prefix(uri,"http://127.0.0.1:1200"))
		{
			GError *error;
			gsize uri_size;
			gchar *shell;
			GString *uri_withsharp,*uri_clean;
			
			gtk_moz_embed_stop_load(GTK_MOZ_EMBED(browser->mozembed));
			shell=g_strconcat(default_browser," ",uri,NULL);

			uri_withsharp=g_string_new(shell);

			uri_size=uri_withsharp->len-2;

			uri_clean=g_string_new_len(shell,uri_size);

			g_spawn_command_line_async(uri_clean->str,NULL);

			g_free(shell);
			g_string_free(uri_withsharp,TRUE);
			g_string_free(uri_clean,TRUE);

			return TRUE;
		}
	}

	return FALSE;
}

gboolean delete_cb(GtkWidget *widget,GdkEventAny *event,PagicoClient *browser)
{
	g_message("delete_cb\n");
	gtk_widget_destroy(browser->window);

	return TRUE;
}

void about_item_activate_cb(GtkWidget *widget,PagicoClient *browser)
{
	GtkWidget *window;
	GtkWidget *image;
	GtkWidget *eventbox;

	window=gtk_window_new(GTK_WINDOW_TOPLEVEL);
	gtk_window_set_title(GTK_WINDOW(window),_("About Pagico"));
	gtk_window_set_resizable(GTK_WINDOW(window),FALSE);
	gtk_window_set_position(GTK_WINDOW(window),GTK_WIN_POS_CENTER_ALWAYS);

	eventbox=gtk_event_box_new();
	gtk_event_box_set_above_child(GTK_EVENT_BOX(eventbox),FALSE);
	g_signal_connect(G_OBJECT(eventbox),"button_press_event",
				G_CALLBACK(button_pressed),window);

	image=gtk_image_new_from_file("/opt/pagico/img/App_GUI/BundleCover/About_Linux.jpg");

	gtk_container_add(GTK_CONTAINER(eventbox),image);
	gtk_container_add(GTK_CONTAINER(window),eventbox);

	gtk_widget_set_events(eventbox,GDK_BUTTON_PRESS_MASK);
	gtk_widget_realize(eventbox);

	gtk_widget_show_all(window);
}

void manual_item_activate_cb(GtkWidget *widget,PagicoClient *browser)
{
	gchar *mime_type;
	gchar *shell;
	const gchar *binary_name;
	GnomeVFSMimeApplication *app;

	mime_type=gnome_vfs_get_mime_type (MANUAL);
	app=gnome_vfs_mime_get_default_application(mime_type);
	binary_name=gnome_vfs_mime_application_get_binary_name(app);	

	shell=g_strconcat(binary_name," ",MANUAL,NULL);	
	g_spawn_command_line_async(shell,NULL);
	
	g_free(shell);
	g_free(mime_type);
	gnome_vfs_mime_application_free(app);
}

void topic_menu_item_activate_cb(GtkWidget *widget,PagicoClient *browser)
{
	uri_item_activate_cb(widget,"http://127.0.0.1:1200/html/?s=11",browser);
}

void contact_menu_item_activate_cb(GtkWidget *widget,PagicoClient *browser)
{
	uri_item_activate_cb(widget,"http://127.0.0.1:1200/html/?s=12",browser);
}

void webiste_menu_item_activate_cb(GtkWidget *widget,PagicoClient *browser)
{
	uri_item_activate_cb(widget,"http://www.pagico.com",browser);
}

void release_menu_item_activate_cb(GtkWidget *widget,PagicoClient *browser)
{
	uri_item_activate_cb(widget,"http://www.pagico.com/releasenote/",browser);
}

void dashboard_menu_item_activate_cb(GtkWidget *widget,PagicoClient *browser)
{
	uri_item_activate_cb(widget,"http://127.0.0.1:1200/html/?s=1",browser);
}

void notes_menu_item_activate_cb(GtkWidget *widget,PagicoClient *browser)
{
	uri_item_activate_cb(widget,"http://127.0.0.1:1200/html/?s=2",browser);
}

void data_menu_item_activate_cb(GtkWidget *widget,PagicoClient *browser)
{
	uri_item_activate_cb(widget,"http://127.0.0.1:1200/html/?s=3",browser);
}

void relations_menu_item_activate_cb(GtkWidget *widget,PagicoClient *browser)
{
	uri_item_activate_cb(widget,"http://127.0.0.1:1200/html/?s=4",browser);
}

void preferences_menu_item_activate_cb(GtkWidget *widget,PagicoClient *browser)
{
	uri_item_activate_cb(widget,"http://127.0.0.1:1200/html/?s=15",browser);
}

void lock_menu_item_activate_cb(GtkWidget *widget,PagicoClient *browser)
{
	uri_item_activate_cb(widget,"http://127.0.0.1:1200/html/login.php?logout",browser);
}

void uri_item_activate_cb(GtkWidget *widget,gchar *uri,PagicoClient *browser)
{
	if(!g_str_has_prefix(uri,"http://127.0.0.1:1200"))
	{
		gchar *shell;

		shell=g_strconcat(default_browser," ",uri,NULL);

		g_spawn_command_line_async(shell,NULL);

		g_free(shell);
	}else{
		gtk_moz_embed_load_url(GTK_MOZ_EMBED(browser->mozembed),uri);
	}
}

gboolean button_pressed(GtkWidget *eventbox,
		GdkEventButton *event,
		GtkWidget *widget)
{
	if(event->type=GDK_BUTTON_PRESS)
	{
		gtk_widget_destroy(widget);

		return TRUE;
	}

	return FALSE;
}
void getcurrentsize(GtkWidget *widget,PagicoClient *browser)
{
	GConfClient *client;
	gint height,width;

	client=gconf_client_get_default();
	gtk_window_get_size(GTK_WINDOW(browser->window),&height,&width);

	g_print("size is %d x %d\n",height,width);

	gconf_client_set_int(client,"/apps/pagico/default_height",height,NULL);
	gconf_client_set_int(client,"/apps/pagico/default_width",width,NULL);
}

void destroy_cb(GtkWidget *widget,PagicoClient *browser)
{
	GList *tmp_list;
	g_message("destroy_cb\n");
	num_browsers--;
	tmp_list=g_list_find(browser_list,browser);
	browser_list=g_list_remove_link(browser_list,tmp_list);

	if(num_browsers==0)
	{
		gtk_main_quit();
	}
}
