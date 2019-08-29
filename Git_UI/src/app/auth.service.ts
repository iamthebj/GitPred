import { Injectable, Input } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Response } from '@angular/http';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  obj:Object[]
  errorMas: boolean =true;
  @Input() sampledata:Object[]
  constructor(private http: HttpClient,private root:Router) {
  }
  submitdata(user_id, password, search_keyword) {
    const body = JSON.stringify({ user_id, password, search_keyword });
    console.log(body);
    const headers: HttpHeaders =
      new HttpHeaders({
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      })
    return this.http.post('http://10.44.126.19:8000/api/connection', body, { headers: headers }).subscribe((data: Response) =>{
       console.log(data);  
       this.obj = data.owner_repositories_list;
      if(data.status == 200){
        this.root.navigate(['/gitrepos']);
       this.errorMas = true;
      }
      this.errorMas = false;
    },err => { console.log(err)});    
  }
}
