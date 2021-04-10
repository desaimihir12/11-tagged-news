#include<bits/stdc++.h>
using namespace std;
int main()
{
    int date,month,year,flag=0;
    cin>>date>>month>>year;
    cout<<"given date = "<<date<<"-"<<month<<"-"<<year<<"\n";
    if(date<1||date>31||month<1||month>12||year<1900||year>2015)
        flag=1;
    int max_days[]={31,28,31,30,31,30,31,31,30,31,30,31};
    if(year%4==0)
        max_days[1]++;
    if(month >0 and month <= 12 and date>max_days[month-1] )
        flag=1;
    if(flag==1)
    {
        cout<<"INVALID\n";
        return 0;
    }
    if(date==1)
    {
        if(month==1)
        {
            date=31;
            month=12;
            year--;
        }
        else
        {
            month--;
            date=max_days[month-1];
        }
    }
    else
    {
        date--;
    }
    cout<<"prevoius date = "<<date<<"-"<<month<<"-"<<year<<"\n";
    


}
