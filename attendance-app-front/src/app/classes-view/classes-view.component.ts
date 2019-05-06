import {Component, OnInit} from '@angular/core';
import {CalendarEvent} from 'angular-calendar';
import {setHours, setMinutes} from 'date-fns';


@Component({
  selector: 'app-classes-view',
  templateUrl: './classes-view.component.html',
  styleUrls: ['./classes-view.component.less']
})
export class ClassesViewComponent implements OnInit {

  constructor() {
  }

  ngOnInit() {
  }

  view: string = 'week';

  viewDate: Date = new Date();

  events: CalendarEvent[] = [
    {
      title: 'TSM',
      color: colors.yellow,
      start: setHours(setMinutes(new Date(), 0), 8),
      end: setHours(setMinutes(new Date(), 30), 9),
      meta: {
        location: "A1"
      }
    },
    {
      title: 'PT',
      color: colors.blue,
      start: setHours(setMinutes(new Date(), 45), 9),
      end: setHours(setMinutes(new Date(), 15), 11),
      meta: {
        location: "L-22"
      }
    },
    {
      title: 'WTI',
      color: colors.red,
      start: setHours(setMinutes(new Date(), 45), 11),
      end: setHours(setMinutes(new Date(), 15), 13),
      meta: {
        location: "M-215"
      }
    },
    {
      title: 'PZ',
      color: colors.green,
      start: setHours(setMinutes(new Date(), 30), 13),
      end: setHours(setMinutes(new Date(), 0), 15),
      meta: {
        location: "210"
      }
    }
  ];

  eventClicked({event}: { event: CalendarEvent }): void {
    console.log('Event clicked', event);
  }
}

export const colors: any = {
  red: {
    primary: '#ad2121',
    secondary: '#FAE3E3'
  },
  blue: {
    primary: '#1e90ff',
    secondary: '#D1E8FF'
  },
  yellow: {
    primary: '#e3bc08',
    secondary: '#FDF1BA'
  },
  green: {
    primary: '#1f9d27',
    secondary: '#94db94'
  }
};
