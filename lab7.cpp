//1
/* #include <iostream>
#include <cmath>
using namespace std;
double s(float a,float b){
    return a+b;
}
int main(){
    int x,y;
    cin>>x>>y;
    cout <<s(x,y);
}
 */
//2
/* #include <iostream>
#include <cmath>
#include <iomanip>
using namespace std;
double hpt(float a,float b){
    return (sqrt((a*a + b*b)));
}
int main(){
float x,y;
cin>>x>>y;
double c=hpt(x,y);
 cout << scientific << setprecision(3) << c;
} */


//3
/*#include <iostream>
#include <cmath>
using namespace std;
double s(float a){
    if(a<0)return a*(-1);
    else return a;
}
int main(){
    int x;
    cin>>x;
    cout <<s(x);
} */


//4
/* #include <iostream>
using namespace std;
string s(int a){
    while(a!=0){
        int f=a%10;
        if(f%2!=0){
            return "Not valid";
        }
        a=a/10;
    }
    return "Valid";
}
int main(){
    int x;
    cin>>x;
    cout <<s(x);
} */

//5
/* #include <iostream>
using namespace std;
bool usnum(int n){
    for(int x:{2,3,5}){
        while(n%x==0)n=n/x;
    }
    return n==1;
}
int main(){
    int a;
    cin>>a;
    if(usnum(a)) cout<<"Yes";
    else cout<<"No";
} */

//6
/* #include <iostream>
using namespace std;
bool luckynum(int n){
    int sum=0;
    int lst=n%10;
    while (n!=0){
        sum+=n%10;
        n=n/10;
    }
    if(sum%lst==0) return true;
    else return false;
}
int main(){
    int a;
    cin>>a;
    if(luckynum(a)) cout<<"Yes";
    else cout<<"No";
} */

//7
/* #include <bits/stdtr1c++.h>
using namespace std;
double f(double a,double b){
    float c=(b*100)/a;
    return c;
}
int main(){
    double x,y;
    cin>>x>>y;
    cout<<f(x,y);
} */
//8
/* #include <bits/stdc++.h>
using namespace std;

bool isprime(int n) {
    if (n <= 1) return false;
    if (n == 2 || n == 3) return true;
    if (n % 2 == 0) return false;

    int s = sqrt(n);

    for (int i = 3; i <= s; i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

int main() {
    int a; 
    cin >> a;
    if (isprime(a)) cout << "Yes";
    else cout << "No";
} */

//9
/* #include <iostream>
/* #include <algorithm>
using  namespace std;1
ъ
void reversing(int a[], int b){
    reverse(a, a+b);
    for(int i=0;i<b;i++){
        cout<<a[i]<<" ";
    }
}
int main(){
    int z;
    cin>>z;
    int n[z];
    for(int i=0;i<z;i++){
        cin>>n[i];
    }
    reversing(n,z);
   
} */ 

//10
/* #include <iostream>
using namespace std;
void reversing(int a[], int b, int w){
    for(int i = 0; i < b; i++){
        if(a[i] == w){
            cout << "yes";
            return;
        }
    }
    cout << "no";
}
int main(){
    int z;
    cin >> z;
    int n[z];
    for(int i = 0; i < z; i++){
        cin >> n[i];
    }
    int y;
    cin >> y;

    reversing(n, z, y);
} */
//11
/* #include <iostream>
using namespace std;
void dino(int a[],int b[]){

}
int mn(){
    int z;
    cin >> z;
    int n[z];
    for(int i = 0; i < z; i++){
        cin >> n[i];
    }
    int a[z];
    for(int i = 0; i < z; i++){
        cin >> z[i];
    }
    int y;
    cin >> y;
}
 */


 //12 
#include <iostream>
using namespace std;
void dino(int z,int a[],int b[]){
    int sum=0;
    for(int i=0;i<z;i++){
        for(int j=0;j<z;j++){
            if(a[i]==b[j]){
                sum++;
            }
        }
    }
    cout<<sum;
} 
int main(){
    int z;
    cin>>z;
    int a[z];
    for(int i = 0; i < z; i++){
        cin >> a[i];
    }
    int b[z];
    for(int i = 0; i < z; i++){
        cin >> b[i];
    }
    dino(z,a,b);
}

