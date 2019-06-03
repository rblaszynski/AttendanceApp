import {Component, OnInit} from '@angular/core';
import {animate, state, style, transition, trigger} from '@angular/animations';
import {MatTableDataSource} from "@angular/material";
import {HttpClient} from "@angular/common/http";
import {UiService} from "../services/ui/ui.service";
import {StudentsService} from "../services/students.service";
import {Student} from "../model/Student";

@Component({
  selector: 'app-students-list',
  templateUrl: './students-list.component.html',
  styleUrls: ['./students-list.component.less'],
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({height: '0px', minHeight: '0', visibility: 'hidden'})),
      state('expanded', style({height: '*', visibility: 'visible'})),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ]),
  ],
})
export class StudentsListComponent implements OnInit {
  displayedColumns = ['id', 'firstName', 'lastName'];
  dataSource: MatTableDataSource<any>;
  file: any;
  fileName: string;
  darkModeActive: boolean;
  students: Student[];
  isExpansionDetailRow = (i: number, row: Object) => {
    return row.hasOwnProperty('detailRow');
  };

  constructor(private http: HttpClient, public ui: UiService, private studentsService: StudentsService) {
  }

  ngOnInit() {
    this.fileName = '';
    this.ui.darkModeState.subscribe((value => {
      this.darkModeActive = value;
    }));
    this.getStudents();
  }

  getStudents(): void {
    this.studentsService.getStudents()
      .subscribe((res: any[]) => {
        this.students = res;
        this.dataSource = new MatTableDataSource(res)
      });
  }

  toggleRow(value: Element) {
    const foundElement = this.dataSource.data.find(elem => elem.element !== undefined && elem.element.id === value.id);
    console.log("The found element is " + JSON.stringify(foundElement));
    const index = this.dataSource.data.indexOf(foundElement);
    this.dataSource.data[index].element.show = !this.dataSource.data[index].element.show;
  }

  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  fileChanged(event) {
    this.file = event.target.files[0];
    this.fileName = this.file.name;
  }

  uploadFile() {
    if (this.file) {
      let fileUploadForm: FormData = new FormData();
      fileUploadForm.append("myFileName", this.file);
      this.studentsService.loadFile(fileUploadForm);
    }
  }
}

export interface Element {
  id: number;
  firstName: string;
  lastName: string;
  groups: string[];
}
