import { Component, OnInit, Output } from '@angular/core';

import { AuthService } from '../auth.service';
import { Router } from '@angular/router';
import { NgForm } from '@angular/forms';
import { NgxSpinnerService } from 'ngx-spinner';
@Component({
  selector: 'app-authentication',
  templateUrl: './authentication.component.html',
  styleUrls: ['./authentication.component.css']
})
export class AuthenticationComponent implements OnInit {
  obj: Object[];
  user_id = "";
  password = "";
  search_keyword = "";
  errorMsg = '';
  constructor(private auth: AuthService, private root: Router, private spinner: NgxSpinnerService) { }

  owner_repositories_list: Object;
  ngOnInit() {

  }
  onSubmit(form: NgForm) {
    let data = {
      "user_id": form.value.user_id,
      "password": form.value.password,
      "search_keyword": form.value.search_keyword
    }
    this.auth.submitdata(data.user_id, data.password, data.search_keyword);
    if (!(this.auth.errorMas)) {
      this.errorMsg = "Failed to login!!   Enter the correct login credentials";
    }
     this.spinner.show();
    setTimeout(() => {
        this.spinner.hide();
    }, 10000);
  }
  remove() {
    this.user_id = "";
    this.password = "";
    this.search_keyword = "";
  }
}
export interface User {
  user_id: string,
  password: string,
  search_keyword: string
}