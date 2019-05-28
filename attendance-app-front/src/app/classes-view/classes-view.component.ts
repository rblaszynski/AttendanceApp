import {Component, OnInit} from '@angular/core';
import {CalendarEvent} from 'angular-calendar';
import {UiService} from "../services/ui/ui.service";
import {ClassesService} from "../services/classes.service";

@Component({
  selector: 'app-classes-view',
  templateUrl: './classes-view.component.html',
  styleUrls: ['./classes-view.component.less']
})
export class ClassesViewComponent implements OnInit {
  darkModeActive: boolean;
  events: CalendarEvent[];

  constructor(public ui: UiService, private classesService: ClassesService) {
  }

  ngOnInit() {
    this.ui.darkModeState.subscribe((value => {
      this.darkModeActive = value;
    }));
    this.getCLasses();
  }

  getCLasses(): void {
    this.classesService.getClasses()
      .subscribe((res: CalendarEvent[]) => {
        res.forEach((item) => {
          item.start = new Date(item.start);
          item.end = new Date(item.end);
        });
        this.events = res;
      })
  }

  view: string = 'week';

  viewDate: Date = new Date();

  eventClicked({event}: { event: CalendarEvent }): void {
    console.log('Event clicked', event);
  }
}
