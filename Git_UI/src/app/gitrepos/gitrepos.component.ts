import { Component, OnInit, Input, Sanitizer, Output, TemplateRef } from '@angular/core';
import { AuthService } from '../auth.service';
import { owner } from '../csvservice';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-gitrepos',
  templateUrl: './gitrepos.component.html',
  styleUrls: ['./gitrepos.component.css']
})
export class GitreposComponent implements OnInit {
  private server_api = 'http://10.44.126.19:8000/api/';
  public loading = false;
  @Input() obj: Object[]
  user = '';
  pass = '';
  serch = '';
  jso: owner[];
  title: String;
  data: any;
  pk: any;
  owner_name: string;
  repository_name: string;
  selectedAll: any;
  sampledata: any;
  errorMsg:any;
  public loadingTemplate: TemplateRef<any>;
  Checks: Array<{ owner_name: string, repository_name: string }> = [];
  sample: any;
  constructor(private api: AuthService, private http: HttpClient) {
  }
  selectAll(event) {
    for (var i = 0; i < this.data.length; i++) {
      this.data[i].selected = this.selectedAll;
    }
    if (event.target.checked) {
      this.sampledata = JSON.stringify(this.data);
       console.log(this.sampledata);
    }
  }
  checkIfAllSelected(event, val) {
    this.selectedAll = this.data.every(function (item: any) {
      return item.selected == false;
    })
    if (event.target.checked) {
      this.Checks.push({ "owner_name": val.owner_name, "repository_name": val.repository_name });
      this.sampledata = JSON.stringify(this.Checks);
      console.log(this.sampledata);
    } 
    else{
      for (var i = 1; i <=this.Checks.length; i++) {
          this.Checks.splice(i,1);
          this.sampledata = JSON.stringify(this.Checks);
          console.log(this.sampledata);
      }
    }
  }
  ngOnInit() {
    this.data = this.api.obj;
  }
  submit(select_value) {
    if (select_value == '1') {
      this.pull_api();
    }
    if (select_value == '2') {
      this.files_api();
    }
  }
  pull_api() {
    this.loading = true;
    const headers: HttpHeaders =
      new HttpHeaders({
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      })
    this.http.post(this.server_api + 'pulls_extract', this.sampledata, { headers: headers, responseType: 'blob' })
      .subscribe(res => {
        this.loading = false;
        this.download(res)
       }, err => {
         this.loading  = false;
        console.log(err);
      })
  }
  download(res: any) {
    var blob = new Blob([res], { type: 'type/zip' });
    console.log(blob);
    var url = window.URL.createObjectURL(blob);
    window.open(url);
  }
  files_api() {
    this.loading = true;
    const headers: HttpHeaders =
      new HttpHeaders({
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      })
    this.http.post(this.server_api + 'files_extract', this.sampledata, { headers: headers, responseType: 'blob' }).
      subscribe(res =>{ 
        this.loading = false;
        this.download1(res)
      }, err => {
        this.loading = false;
        console.log(err);
      })
  }
  download1(res: any) {
    var blob = new Blob([res], { type: 'type/zip' });
    console.log(blob);
    var url = window.URL.createObjectURL(blob);
    window.open(url);
  }
}
