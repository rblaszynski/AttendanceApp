import {Component, OnInit} from '@angular/core';
import {animate, state, style, transition, trigger} from '@angular/animations';
import {MatTableDataSource} from "@angular/material";
import {HttpClient} from "@angular/common/http";

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
  isExpansionDetailRow = (i: number, row: Object) => {
    return row.hasOwnProperty('detailRow');
  };

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.dataSource = new MatTableDataSource(this.getRows());
    this.fileName = '';
  }

  getRows() {
    const rows = [];
    data.forEach(element => rows.push(element, {detailRow: true, element}));
    console.log(rows);
    return rows;
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
      this.http
        .post("http://localhost:4200/api", fileUploadForm)
        .subscribe(response => {
          //handle response
        }, err => {
          //handle error
        });
    }
  }


}

export interface Element {
  id: number;
  firstName: string;
  lastName: string;
  groups: string[];
}

const data: Element[] = [
  {id: 111111, firstName: 'Michał', lastName: 'Andrzejewski', groups: ['PT-1', 'PZ-1']},
  {id: 222222, firstName: 'Przemysław', lastName: 'Barłóg', groups: ['PT-1', 'PZ-1']},
  {id: 333333, firstName: 'Dominik', lastName: 'Błaszczyk', groups: ['PT-2', 'PZ-2']},
  {id: 444444, firstName: 'Robert', lastName: 'Błaszyński', groups: ['PT-2', 'PZ-2']},
];
