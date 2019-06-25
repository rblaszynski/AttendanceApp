import {Component, OnInit} from '@angular/core';
import {SelectionModel} from '@angular/cdk/collections';
import {MatTableDataSource} from '@angular/material';
import {UiService} from "../services/ui/ui.service";
import {RecentLabsService} from "../services/recent-labs.service";
import {Lecture} from "../model/Lecture";

export interface PeriodicElement {
  id: number;
  firstName: string;
  lastName: string;
  group: string;
  isPresent: boolean;
  nr_indeksu: number;
}

@Component({
  selector: 'app-attendance-table',
  templateUrl: './attendance-table.component.html',
  styleUrls: ['./attendance-table.component.less']
})
export class AttendanceTableComponent implements OnInit {
  displayedColumns: string[] = ['select', 'nr_indeksu', 'firstName', 'lastName', 'group', 'isPresent'];
  dataSource: MatTableDataSource<PeriodicElement>;
  selection = new SelectionModel<PeriodicElement>(true, []);
  darkModeActive: boolean;
  className: string;
  classGroupName: string;
  classStartDate: Date;
  classEndDate: Date;

  constructor(public ui: UiService, private recentLabsService: RecentLabsService) {

  }

  ngOnInit() {
    this.ui.darkModeState.subscribe((value => {
      this.darkModeActive = value;
    }));
    this.getRecentLabs();
  }

  getRecentLabs(): void {
    this.recentLabsService.getRecentLabs()
      .subscribe((res: Lecture) => {
        this.className = res.className;
        this.classGroupName = res.classGroupName;
        this.classStartDate = res.classStartDate;
        this.classEndDate = res.classEndDate;
        this.dataSource = new MatTableDataSource<PeriodicElement>(res.studentsList);
        this.dataSource.data.forEach(row => {
          if (row.isPresent) {
            this.selection.select(row)
          }
        });
      })
  }

  updateRecentLabs(): void {
    this.recentLabsService.updateRecentLabs(this.dataSource.filteredData).subscribe((res) => {
      console.log(res);
      this.dataSource.filteredData = res;
    });
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
    row.isPresent = this.selection.isSelected(row);
    return `${this.selection.isSelected(row) ? 'deselect' : 'select'} row ${row.id + 1}`;
  }
}
