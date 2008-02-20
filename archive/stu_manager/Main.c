#include<stdio.h>
#include<string.h>
/*@author TualatriX
/*@data 2007.1.10
/*@Version 1.0
*/
struct student{
        int visible;
        int num;
        char name[10];
        char place[6];
}stu[30];int TOTAL=sizeof(stu)/sizeof(struct student);

print_star(){
        int i=0;
        for(;i<50;i++){
                printf("*");
        }
        printf("\n");
}

print_minus(){
        int i=0;
        for(;i<50;i++){
                printf("-");
        }
        printf("\n");
}

print_sort_start(){
	int totalnum;
        print_minus();
        totalnum=show_remain();
        printf("��Ҫ�����¼�¼������������\n");
        show_all();
        printf("��Ҫ����%d����¼��\n",totalnum);
        print_minus();
        printf("����������......\n");
}

print_sort_end(){
        printf("������ϡ�\n");
        show_all();
        printf("����������õļ�¼��\n");
}

show_remain(){
        int i=0,count=0;
        for(;i<=TOTAL-1;i++){
                if(stu[i].visible==1){
                	count++;
        	}
        }
        printf("һ����%d����¼�ռ䣬���й�%d�������ü�¼��\n",TOTAL,count);
        return count;
}

add(){
        int choice;			
        while(1){
                printf("====================���Ӽ�¼ģ��====================\n");
                show_remain();
		print_used();
                printf("\n1���������Ӽ�¼��0���˳�[1/0]");
                scanf("%d",&choice);
                switch(choice){
                case 0:system("cls");return 0; break;
                case 1:system("cls");add_data();break;
        	}
        }
}

print_used(){
	int i;
	for(i=0;i<TOTAL;i++){
		if(stu[i].visible==1){
			printf("%d ",i);
		}
		else printf("- ");
	}
}

add_data(){
        int s,i,e=TOTAL;
        char c;
	print_minus();
        printf("��Ҫ�ӵڼ�����¼��ʼ׷��?��0Ϊ��ʼ��)��");
        scanf("%d",&s);
        printf("��Ҫ׷�ӵ��ڼ�����¼?��%dΪ��ֹ��)��",TOTAL-1);
        scanf("%d",&e);
        i=s;
        printf("һ��Ҫ׷��%d����¼��\n",e-s+1);
        for(;s<=e;s++,i++){
                print_minus();
loop:        printf("�������%d��ѧ����ѧ�ţ�",s+1);
                scanf("%d",&stu[i].num);
                stu[i].visible=1;
		if(return_only_num(i,stu[i].num)==1){
			printf("�Բ��𣬴�ѧ��������ѧ���ظ��������䣡\n");
			goto loop;
		}
                printf("���֣�");
                scanf("%s",stu[i].name);
                printf("���᣺");
                scanf("%s",stu[i].place);
        }
        print_minus();
	printf("������ʹ�õļ�¼��");
	print_used();
        printf("\n׷����ϣ��ַ��ء�\n");
}

modify(){
        int choice;
        while(1){
                printf("====================�޸ļ�¼ģ��====================\n");
                show_remain();
                printf("1������¼�����޸ģ�2����ѧ�����޸ģ�3�����������޸ģ�0���˳�[1/2/3/0]");
                scanf("%d",&choice);
                switch(choice){
                case 0:system("cls");return 0;break;
                case 1:system("cls");modify_id();break;
                case 2:system("cls");modify_num();break;
                case 3:system("cls");modify_name();break;
        	}
        }
}

modify_single(int i){
        print_minus();
        printf("�������%d��ѧ����ѧ��(ԭѧ����%d)��",i+1,stu[i].num);
        scanf("%d",&stu[i].num);
        printf("����(ԭ������%s)��",stu[i].name);
        scanf("%s",stu[i].name);
        printf("����(ԭ������%s)��",stu[i].place);
        scanf("%s",stu[i].place);
        stu[i].visible=1;
        show_id(i);
}

modify_num(){
        int i;
        i=search_num();
	if(i!=0){
		modify_single(i);
	}
}

modify_id(){
        int i;
        print_star();
        printf("��������Ҫ�޸ĵڼ�����¼��");
        scanf("%d",&i);
        show_id(i);
        modify_single(i);
        printf("�޸����!��Ҫ�����޸�������׷�Ӽ�¼����\n");
}

modify_name(){
        int i;
        i=search_name();
        modify_single(i);
}

show_id(int i){
        printf("��¼��.%d ѧ��:%d ����:%s ����:%s \n",i,stu[i].num,stu[i].name,stu[i].place);
}

del(){
        int choice;
        while(1){
                printf("====================ɾ����¼ģ��==================\n");
                printf("1��ȫ��ɾ����2������ɾ����3������¼��ɾ����4��������ɾ����0.�˳�[1/2/3/0]");
                scanf("%d",&choice);
                switch(choice){
                        case 0:system("cls");return 0;break;
                        case 1:system("cls");del_all();break;
                        case 2:system("cls");del_batch();break;
                        case 3:system("cls");del_id();break;
                        case 4:system("cls");del_name();break;
        	}
        }
}

del_all(){
        char c;
        print_minus();
        printf("���棻��Ҫɾ��ȫ����¼��[y/n]");
        while(1){
                scanf("%c",&c);
                switch(c){
                        case 'y':system("cls");del_all_core();return 0;break;
                        case 'n':system("cls");return 0;break;
                }
        }
}

del_all_core(){
        int i;
        printf("����ɾ��������\n");
        for(i=0;i<30;i++){
                stu[i].visible=0;
                printf("stu[%d]��ɾ����",i);
        }
        printf("\n");
        print_minus();
        printf("�Ѿ�ȫ��ɾ����ϡ�\n");
        show_remain();
}

del_batch(){
        int i,j;
        print_minus();
	print_used();
        printf("��������Ҫ����ɾ������ʼ��¼�ź���ֹ��¼��:[i,j]");
        scanf("%d,%d",&i,&j);
        printf("����ɾ��������\n");
        for(;i<=j;i++){
                stu[i].visible=0;
                printf("stu[%d]��ɾ��.",i);
        }
        printf("�Ѿ�ɾ����ϡ�\n");
        show_remain();
}

del_id(){
        int i;
        print_minus();
        printf("��������Ҫɾ���ļ�¼�ţ�");
        scanf("%d",&i);
        stu[i].visible=0;
        printf("�ѽ�stu[%d]�����¼ɾ����\n",i);
        show_remain();
}

del_name(){
        int i;
        i=search_name();
        stu[i].visible=0;
        printf("�ѽ�stu[%d]�����¼ɾ����\n",i);
        show_remain();
}

search(){
        int choice;
        while(1){	
                printf("====================������¼ģ��====================\n");
                printf("1����ʾȫ����¼��2������¼�Ų��ң�3����ѧ�Ų��ң�4�����������ң�0���˳�[1/2/3/4/0]");
                scanf("%d",&choice);
                switch(choice){
                        case 0:system("cls");return 0;break;
                        case 1:system("cls");show_remain();show_all();break;
                        case 2:system("cls");search_id();break;
                        case 3:system("cls");search_num();break;
                        case 4:system("cls");search_name();break;
        	}
        }
}

search_id(){
        int i;
        print_minus();
        printf("��������Ҫ��ѯ�ļ�¼�ţ�");
        scanf("%d",&i);
	if(stu[i].visible==0){
		printf("�Բ���û�����¼��\n");
	}
	else {
		show_id(i);
		printf("��ѯ��ϣ����ء�\n");
	}
}

search_num(){
        int i=0,count=0;
        int num;
        print_minus();
        printf("��������Ҫ��ѯ��ѧ�ţ�");
        scanf("%d",&num);
        printf("Ҫ���ҵ�ѧ���ǣ�%d\n",num);
        for(;i<TOTAL;i++){
                if(stu[i].visible==1){
                                if(stu[i].num==num){
                			count++;
                			show_id(i);
                			return i;
        			}
        return 0;			
        	}
        }
        if(count==0)printf("�Բ����Ҳ�����\n");
        printf("��ѯ��ϣ����ء�\n");
}

return_only_num(int i,int num){
	int j=0;
	for(;j<TOTAL;j++){
		if(i==j){
			continue;
		}
		else if(stu[j].visible==1){
			if(stu[j].num==num){
				return 1;
				break;
			}
		}
	}
	return 0;
}

search_name(){
        int i,count=0;
        char c[10];
        print_minus();
        printf("��������Ҫ��ѯ��������");
        scanf("%s",&c);
        printf("Ҫ���ҵ������ǣ�%s\n",c);
        for(i=0;i<TOTAL;i++){
                if(stu[i].visible==1){
                                if(!(strcmp(stu[i].name,c))){
                			count++;
                			show_id(i);
                			return i;
        			}
        	}
        }
        if(count==0)printf("�Բ����Ҳ���.\n");
        printf("��ѯ��ϣ����ء�\n");
}

show_all(){
        int i;
        print_minus();
        print_used();
        printf("\n");
        for(i=0;i<TOTAL;i++){
                if(stu[i].visible==1)show_id(i);
        }
        print_minus();
        printf("��ʾ��ϣ����ء�\n");
}

sort(){
        int choice;
        while(1){	
                printf("====================�����¼ģ��====================\n");
                printf("1����ѧ�Ž�����������2����ѧ�Ž��н�������0���˳�[1/2/0]");
                scanf("%d",&choice);
                switch(choice){
                        case 0:system("cls");return 0;break;
                        case 1:system("cls");sort_up();break;
                        case 2:system("cls");sort_down();break;
        	}
        }
}

sort_up(){
	struct student temp;
        int i,j;
	print_sort_start();
         for(j=1;j<TOTAL;j++){
                for(i=0;i<TOTAL-j;i++){
                        if(stu[i].num>stu[i+1].num){
                                temp=stu[i+1];
                                stu[i+1]=stu[i];
                                stu[i]=temp;
                        }
                }
        }
	print_sort_end();
}

sort_down(){
	struct student temp;
        int i,j;
	print_sort_start();
         for(j=1;j<TOTAL;j++){
                for(i=0;i<TOTAL-j;i++){
                        if(stu[i].num<stu[i+1].num){
                                temp=stu[i+1];
                                stu[i+1]=stu[i];
                                stu[i]=temp;
                        }
                }
        }
	print_sort_end();
}

file(){
        int choice;
        while(1){	
                printf("====================�ļ�����ģ��====================\n");
                printf("1��д���ļ���2����ȡ�ļ���0���˳�[1/2/0]");
                scanf("%d",&choice);
                switch(choice){
                        case 0:system("cls");return 0;break;
                        case 1:system("cls");file_write();break;
                        case 2:system("cls");file_read();break;
        	}
        }
}

file_write(){
        int i;
        FILE *fp;
        fp=fopen("stud.dat","w");
        for(i=0;i<TOTAL;i++){
                if(fwrite(&stu[i],sizeof(struct student),1,fp)!=1){
                        printf("�ļ�д�����\n");
                }
        }
        printf("�ļ�д��ɹ�!��д��\"stud.dat\"��\n");
}

file_read(){
        int i;
        FILE *fp;
        if((fp=fopen("stud.dat","r+"))==NULL){
                printf("���ܴ��ļ���\n");
                return 0;
        }
        for(i=0;fread(&stu[i],sizeof(struct student),1,fp)!=0;i++){
         }
        printf("�ļ�'stud.dat'�Ѷ��롣\n");
         
}
main()
{
        int select;
	system("cls");
        while(1){
                printf("******************************��ӭ����ѧ������ϵͳ******************************\n");
                printf("                                                                      Verion 1.0\n\n");
                printf("                              1.=>׷�Ӽ�¼<=\n");
                printf("                              2.=>�޸ļ�¼<=\n");
                printf("                              3.=>��ѯ��¼<=\n");
                printf("                              4.=>ɾ����¼<=\n");
                printf("                              5.=>�����¼<=\n");
                printf("                              6.=>�ļ�����<=\n");
                printf("                              0.=>!!�˳�!!<=\n");
                printf("\n\nע��Ϊ�˷���C���Ե�ϰ�ߣ����������йء���¼�š�����ֵ�����Ǵ�0��ʼ�ġ�\n");
                print_minus();
                printf("ѡ����Ҫ����Ĳ˵��������빦�ܺ�[1/2/3/4/5/0]");
                scanf("%d",&select);
                switch(select){
                        case 0:return 0;
                        case 1:system("cls");add();break;
                        case 2:system("cls");modify();break;
                        case 3:system("cls");search();break;
                        case 4:system("cls");del();break;
                        case 5:system("cls");sort();break;
                        case 6:system("cls");file();break;
        }
    }
}
