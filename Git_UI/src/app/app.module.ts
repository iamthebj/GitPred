import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { AuthenticationComponent } from './authentication/authentication.component';
import { GitreposComponent } from './gitrepos/gitrepos.component';
import { FormsModule } from '@angular/forms';
import { RouterModule,Router, Routes} from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import {NgxPaginationModule} from 'ngx-pagination';
import { NgxLoadingModule,ngxLoadingAnimationTypes } from 'ngx-loading';
import { NgxSpinnerModule } from 'ngx-spinner';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AuthService } from './auth.service';


const app : Routes=[
  {
    path:'',
    component:AuthenticationComponent
  },
  {
    path:'gitrepos',
    component:GitreposComponent
  }
 ]
@NgModule({
  declarations: [
    AppComponent,
    AuthenticationComponent,
    GitreposComponent,
  
  ],
  imports: [
    BrowserModule,
    FormsModule,
    RouterModule.forRoot(app),
    HttpClientModule,
    NgxPaginationModule,
    NgxLoadingModule.forRoot({
      animationType: ngxLoadingAnimationTypes.wanderingCubes,
        backdropBackgroundColour: 'rgba(255, 255, 255, 0.8)', 
        backdropBorderRadius: '4px',
        primaryColour: '#000000', 
        secondaryColour: '#000000', 
        tertiaryColour: '#000000',
        width:'100%',
        height:'100%',
    }),
    NgxSpinnerModule,
    BrowserModule,
    BrowserAnimationsModule
  ],
  providers: [AuthService],
  bootstrap: [AppComponent]
})
export class AppModule { }
