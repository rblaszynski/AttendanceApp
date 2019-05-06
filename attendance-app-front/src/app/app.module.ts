import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {UiService} from "./services/ui/ui.service";
import {AttendanceTableComponent} from './attendance-table/attendance-table.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {FormsModule} from "@angular/forms";
import {CalendarModule, DateAdapter} from 'angular-calendar';
import {adapterFactory} from 'angular-calendar/date-adapters/date-fns';

import {
  MatButtonModule,
  MatCheckboxModule,
  MatFormFieldModule,
  MatIconModule,
  MatInputModule,
  MatRadioModule,
  MatSelectModule,
  MatTableModule
} from "@angular/material";
import {HomeComponent} from './home/home.component';
import {ReportComponent} from './report/report.component';
import {StudentsListComponent} from './students-list/students-list.component';
import {ClassesViewComponent} from './classes-view/classes-view.component';
import {CalendarHeaderComponent} from './calendar-header/calendar-header.component';
import {HttpClientModule} from "@angular/common/http";


@NgModule({
  declarations: [
    AppComponent,
    AttendanceTableComponent,
    HomeComponent,
    ReportComponent,
    StudentsListComponent,
    ClassesViewComponent,
    CalendarHeaderComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatTableModule,
    MatCheckboxModule,
    MatButtonModule,
    MatRadioModule,
    MatFormFieldModule,
    MatSelectModule,
    FormsModule,
    MatIconModule,
    HttpClientModule,
    CalendarModule.forRoot({
      provide: DateAdapter,
      useFactory: adapterFactory
    }),
    MatInputModule,
  ],
  providers: [
    UiService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
