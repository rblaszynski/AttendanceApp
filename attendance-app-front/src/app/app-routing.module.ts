import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {AttendanceTableComponent} from "./attendance-table/attendance-table.component";
import {StudentsListComponent} from "./students-list/students-list.component";
import {ReportComponent} from "./report/report.component";
import {HomeComponent} from "./home/home.component";
import {ClassesListComponent} from "./classes-list/classes-list.component";

const routes: Routes = [
  {path: '', component: HomeComponent},
  {path: 'recent', component: AttendanceTableComponent},
  {path: 'classes', component: ClassesListComponent},
  {path: 'students', component: StudentsListComponent},
  {path: 'reports', component: ReportComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
