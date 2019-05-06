import {Component, OnInit} from '@angular/core';
import {SelectionModel} from '@angular/cdk/collections';
import {MatTableDataSource} from '@angular/material';
import {UiService} from "../services/ui/ui.service";


export interface PeriodicElement {
  index: number;
  firstName: string;
  lastName: string;
  group: string;
}

const ELEMENT_DATA: PeriodicElement[] = [
  {index: 111111, firstName: 'Michał', lastName: 'Andrzejewski', group: 'TI-1'},
  {index: 222222, firstName: 'Przemysław', lastName: 'Barłóg', group: 'TI-1'},
  {index: 333333, firstName: 'Dominik', lastName: 'Błaszczyk', group: 'TI-1'},
  {index: 444444, firstName: 'Robert', lastName: 'Błaszyński', group: 'TI-1'},

];


@Component({
  selector: 'app-attendance-table',
  templateUrl: './attendance-table.component.html',
  styleUrls: ['./attendance-table.component.less']
})
export class AttendanceTableComponent implements OnInit{
  displayedColumns: string[] = ['select', 'index', 'firstName', 'lastName', 'group'];
  dataSource = new MatTableDataSource<PeriodicElement>(ELEMENT_DATA);
  selection = new SelectionModel<PeriodicElement>(true, []);
  darkModeActive: boolean;
  className = 'Sample className';
  classGroupName = "PT_01";
  classStartDate = new Date();
  classEndDate = new Date().setHours(this.classStartDate.getHours()+1, this.classStartDate.getMinutes()+30);

  constructor(public ui: UiService) {

  }

  ngOnInit() {
    this.ui.darkModeState.subscribe((value => {
      this.darkModeActive = value;
    }))
  }

  /** Whether the number of selected elements matches the total number of rows. */
  isAllSelected() {
    const numSelected = this.selection.selected.length;
    const numRows = this.dataSource.data.length;
    return numSelected === numRows;
  }

  /** Selects all rows if they are not all selected; otherwise clear selection. */
  masterToggle() {
    this.isAllSelected() ?
      this.selection.clear() :
      this.dataSource.data.forEach(row => this.selection.select(row));
  }

  /** The label for the checkbox on the passed row */
  checkboxLabel(row?: PeriodicElement): string {
    if (!row) {
      return `${this.isAllSelected() ? 'select' : 'deselect'} all`;
    }
    return `${this.selection.isSelected(row) ? 'deselect' : 'select'} row ${row.index + 1}`;
  }
}
