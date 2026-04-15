/* #include <iostream>
#include <vector>
using namespace std;
int main(){                                  
    vector <int>m;
    int x;
    while(cin>>x){
        m.push_back(x);
    }
    cout<<m.size();
} */

//806
/* #include <iostream>
#include <vector>
using namespace std;;
int main(){
    int n;
    cin>>n;
    vector<int>s;
    for(int i=0;i<n;i++){
        int x;
        cin>>x;
        s.push_back(x); 
    }
    int md;
    int mcnt=0;
    for(int i=0;i<n;i++){
        int cnt=0;
        for (int j=0;j<n;j++){
            if(s[j]==s[i]){
                cnt++;            
            }
        }
    if (cnt > mcnt || (cnt == mcnt && s[i] < md)){
        md=s[i];
        mcnt=cnt;
    };
    }   
    cout<<md;
} 
 */
/* 
 #include <iostream>
#include <vector>
using namespace std;;
int main(){
    int n;
    cin>>n;
    vector<int>s;
    for(int i=0;i<n;i++){
        int x;
        cin>>x;
        s.push_back(x); 
    }
    for(int i=0;i<n;i++){
        cout<<s[i];
    }
} 
*/
/* #include <iostream>
#include <set>
using namespace std;
int main(){
    int n;
    cin>>n;
    set<int>d;
    for (int i=0;i<n;i++){
        int x;
        cin>>x;
        d.insert(x);
    }
    for (int x:d){
        cout<<x<<" ";
    }
}
 */

/* 
 #include <iostream>
 #include <set>
 using namespace std;
 int main(){
    int n;
    cin>>n;
    set<int>dino;
    for(int i=0;i<n;i++){
        int x;
        cin>>x;
        dino.insert(x);
    }
    cout<<dino.size();
 }
 */
 #include <iostream>
 #include <string>
 #include <algorithm>
 using namespace std;
 int main(){
    string n,m;
    cin>>n>>m;
    sort(n);
    sort(m);
    for(int i=0;i<n;i++){
        if(n[i]!=m[i]){
            
        }
    }
 }