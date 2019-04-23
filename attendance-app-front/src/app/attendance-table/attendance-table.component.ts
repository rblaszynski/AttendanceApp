import {Component} from '@angular/core';
import {SelectionModel} from '@angular/cdk/collections';
import {MatTableDataSource} from '@angular/material';

export interface PeriodicElement {
  firstName: string;
  lastName: string;
  indexNr: number;
  group: string;
}

const ELEMENT_DATA: PeriodicElement[] = [
  {indexNr: 111111, firstName: 'Michał', lastName: 'Andrzejewski', group: 'TI-1'},
  {indexNr: 222222, firstName: 'Przemysław', lastName: 'Barłóg', group: 'TI-1'},
  {indexNr: 333333, firstName: 'Dominik', lastName: 'Błaszczyk', group: 'TI-1'},
  {indexNr: 444444, firstName: 'Robert', lastName: 'Błaszyński', group: 'TI-1'},

];


@Component({
  selector: 'app-attendance-table',
  templateUrl: './attendance-table.component.html',
  styleUrls: ['./attendance-table.component.less']
})
export class AttendanceTableComponent {
  displayedColumns: string[] = ['select', 'position', 'name', 'weight', 'symbol'];
  dataSource = new MatTableDataSource<PeriodicElement>(ELEMENT_DATA);
  selection = new SelectionModel<PeriodicElement>(true, []);

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
    return `${this.selection.isSelected(row) ? 'deselect' : 'select'} row ${row.indexNr + 1}`;
  }
}
