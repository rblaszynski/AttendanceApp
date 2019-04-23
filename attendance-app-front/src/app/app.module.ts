import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {UiService} from "./services/ui/ui.service";
import {AttendanceTableComponent} from './attendance-table/attendance-table.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatButtonModule, MatCheckboxModule, MatTableModule} from "@angular/material";
import {HomeComponent} from './home/home.component';
import {ReportComponent} from './report/report.component';
import {StudentsListComponent} from './students-list/students-list.component';
import {ClassesListComponent} from './classes-list/classes-list.component';


@NgModule({
  declarations: [
    AppComponent,
    AttendanceTableComponent,
    HomeComponent,
    ReportComponent,
    StudentsListComponent,
    ClassesListComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatTableModule,
    MatCheckboxModule,
    MatButtonModule
  ],
  providers: [
    UiService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
