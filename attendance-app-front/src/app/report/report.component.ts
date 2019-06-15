import {Component, OnInit} from '@angular/core';
import {ReportsService} from "../services/reports.service";
import {StudentsService} from "../services/students.service";
import {Student} from "../model/Student";

@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.less']
})
export class ReportComponent implements OnInit {
  students: Student[];
  classes: Class[] = [
    {id: '1', viewValue: 'PT-1'},
    {id: '2', viewValue: 'PT-2'},
    {id: '3', viewValue: 'TSM-1'},
    {id: '4', viewValue: 'TSM-2'}
  ];
  reportId: number;
  reportType: string;
  selected: string;

  constructor(private reportService: ReportsService, private studentsService: StudentsService) {
  }

  ngOnInit() {
    this.selected = null;
    this.getStudents();
    this.reportType = '';
    this.reportId = null;
  }

  getStudents(): void {
    this.studentsService.getStudents()
      .subscribe((res: any[]) => {
        this.students = res;
      });
  }

  generateReport() {
    const report: Report = {id: this.reportId, type: this.selected};
    this.reportService.generateReport(report);
  }
}

export interface Class {
  id: string;
  viewValue: string;
}

export interface Report {
  id: number;
  type: string;
}
