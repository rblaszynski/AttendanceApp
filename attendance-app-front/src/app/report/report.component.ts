import {Component, OnInit} from '@angular/core';

@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.less']
})
export class ReportComponent implements OnInit {
  students: Student[] = [
    {id: '111', viewValue: 'Michal Andrzejewski'},
    {id: '222', viewValue: 'Dominik Błaszczyk'},
    {id: '333', viewValue: 'Przemysław Barłóg'},
    {id: '444', viewValue: 'Robert Błaszyński'}
  ];
  classes: Class[] = [
    {id: '1', viewValue: 'PT-1'},
    {id: '2', viewValue: 'PT-2'},
    {id: '3', viewValue: 'TSM-1'},
    {id: '4', viewValue: 'TSM-2'}
  ];
  selected: string;
  constructor() { }

  ngOnInit() {
    this.selected = null;
  }

}
export interface Student {
  id: string;
  viewValue: string;
}

export interface Class {
  id: string;
  viewValue: string;
}
