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
        printf("将要对以下记录进行升序排序：\n");
        show_all();
        printf("共要排序%d个记录。\n",totalnum);
        print_minus();
        printf("正在排序中......\n");
}

print_sort_end(){
        printf("排序完毕。\n");
        show_all();
        printf("以上是排序好的记录。\n");
}

show_remain(){
        int i=0,count=0;
        for(;i<=TOTAL-1;i++){
                if(stu[i].visible==1){
                	count++;
        	}
        }
        printf("一共有%d个记录空间，其中共%d个是已用记录。\n",TOTAL,count);
        return count;
}

add(){
        int choice;			
        while(1){
                printf("====================增加记录模块====================\n");
                show_remain();
		print_used();
                printf("\n1、继续增加记录；0、退出[1/0]");
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
        printf("你要从第几个记录开始追加?（0为起始数)：");
        scanf("%d",&s);
        printf("你要追加到第几个记录?（%d为终止数)：",TOTAL-1);
        scanf("%d",&e);
        i=s;
        printf("一共要追加%d个记录。\n",e-s+1);
        for(;s<=e;s++,i++){
                print_minus();
loop:        printf("请输入第%d个学生的学号：",s+1);
                scanf("%d",&stu[i].num);
                stu[i].visible=1;
		if(return_only_num(i,stu[i].num)==1){
			printf("对不起，此学号与已有学号重复，请重输！\n");
			goto loop;
		}
                printf("名字：");
                scanf("%s",stu[i].name);
                printf("籍贯：");
                scanf("%s",stu[i].place);
        }
        print_minus();
	printf("现在已使用的记录：");
	print_used();
        printf("\n追加完毕，现返回。\n");
}

modify(){
        int choice;
        while(1){
                printf("====================修改记录模块====================\n");
                show_remain();
                printf("1、按记录号来修改；2、按学号来修改；3、按姓名来修改；0、退出[1/2/3/0]");
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
        printf("请输入第%d个学生的学号(原学号是%d)：",i+1,stu[i].num);
        scanf("%d",&stu[i].num);
        printf("姓名(原姓名是%s)：",stu[i].name);
        scanf("%s",stu[i].name);
        printf("籍贯(原籍贯是%s)：",stu[i].place);
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
        printf("请输入你要修改第几个记录：");
        scanf("%d",&i);
        show_id(i);
        modify_single(i);
        printf("修改完成!如要批量修改请至“追加记录处”\n");
}

modify_name(){
        int i;
        i=search_name();
        modify_single(i);
}

show_id(int i){
        printf("记录号.%d 学号:%d 姓名:%s 籍贯:%s \n",i,stu[i].num,stu[i].name,stu[i].place);
}

del(){
        int choice;
        while(1){
                printf("====================删除记录模块==================\n");
                printf("1、全部删除；2、批量删除；3、按记录号删除；4、按姓名删除；0.退出[1/2/3/0]");
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
        printf("警告；将要删除全部记录！[y/n]");
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
        printf("正在删除。。。\n");
        for(i=0;i<30;i++){
                stu[i].visible=0;
                printf("stu[%d]已删除。",i);
        }
        printf("\n");
        print_minus();
        printf("已经全部删除完毕。\n");
        show_remain();
}

del_batch(){
        int i,j;
        print_minus();
	print_used();
        printf("请输入你要批量删除的起始记录号和终止记录号:[i,j]");
        scanf("%d,%d",&i,&j);
        printf("正在删除。。。\n");
        for(;i<=j;i++){
                stu[i].visible=0;
                printf("stu[%d]已删除.",i);
        }
        printf("已经删除完毕。\n");
        show_remain();
}

del_id(){
        int i;
        print_minus();
        printf("请输入你要删除的记录号：");
        scanf("%d",&i);
        stu[i].visible=0;
        printf("已将stu[%d]这个记录删除。\n",i);
        show_remain();
}

del_name(){
        int i;
        i=search_name();
        stu[i].visible=0;
        printf("已将stu[%d]这个记录删除。\n",i);
        show_remain();
}

search(){
        int choice;
        while(1){	
                printf("====================搜索记录模块====================\n");
                printf("1、显示全部记录；2、按记录号查找；3、按学号查找；4、按姓名查找；0、退出[1/2/3/4/0]");
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
        printf("请输入你要查询的记录号：");
        scanf("%d",&i);
	if(stu[i].visible==0){
		printf("对不起，没有这记录。\n");
	}
	else {
		show_id(i);
		printf("查询完毕，返回。\n");
	}
}

search_num(){
        int i=0,count=0;
        int num;
        print_minus();
        printf("请输入你要查询的学号：");
        scanf("%d",&num);
        printf("要查找的学号是：%d\n",num);
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
        if(count==0)printf("对不起，找不到。\n");
        printf("查询完毕，返回。\n");
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
        printf("请输入你要查询的姓名：");
        scanf("%s",&c);
        printf("要查找的姓名是：%s\n",c);
        for(i=0;i<TOTAL;i++){
                if(stu[i].visible==1){
                                if(!(strcmp(stu[i].name,c))){
                			count++;
                			show_id(i);
                			return i;
        			}
        	}
        }
        if(count==0)printf("对不起，找不到.\n");
        printf("查询完毕，返回。\n");
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
        printf("显示完毕，返回。\n");
}

sort(){
        int choice;
        while(1){	
                printf("====================排序记录模块====================\n");
                printf("1、以学号进行升序排序；2、以学号进行降序排序；0、退出[1/2/0]");
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
                printf("====================文件操作模块====================\n");
                printf("1、写入文件；2、读取文件；0、退出[1/2/0]");
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
                        printf("文件写入错误！\n");
                }
        }
        printf("文件写入成功!已写入\"stud.dat\"！\n");
}

file_read(){
        int i;
        FILE *fp;
        if((fp=fopen("stud.dat","r+"))==NULL){
                printf("不能打开文件！\n");
                return 0;
        }
        for(i=0;fread(&stu[i],sizeof(struct student),1,fp)!=0;i++){
         }
        printf("文件'stud.dat'已读入。\n");
         
}
main()
{
        int select;
	system("cls");
        while(1){
                printf("******************************欢迎进入学籍管理系统******************************\n");
                printf("                                                                      Verion 1.0\n\n");
                printf("                              1.=>追加记录<=\n");
                printf("                              2.=>修改记录<=\n");
                printf("                              3.=>查询记录<=\n");
                printf("                              4.=>删除记录<=\n");
                printf("                              5.=>排序记录<=\n");
                printf("                              6.=>文件操作<=\n");
                printf("                              0.=>!!退出!!<=\n");
                printf("\n\n注：为了符合C语言的习惯，里面所有有关“记录号”的数值，都是从0开始的。\n");
                print_minus();
                printf("选择您要进入的菜单，请输入功能号[1/2/3/4/5/0]");
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
