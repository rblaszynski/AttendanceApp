import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {UiService} from "../services/ui/ui.service";

@Component({
  selector: 'mwl-demo-utils-calendar-header',
  templateUrl: './calendar-header.component.html',
  styleUrls: ['./calendar-header.component.less']
})
export class CalendarHeaderComponent implements OnInit {
  darkModeActive: boolean;
  constructor(public ui: UiService) {}

  ngOnInit() {
    this.ui.darkModeState.subscribe((value => {
      this.darkModeActive = value;
    }))
  }

  @Input() view: string;

  @Input() viewDate: Date;

  @Input() locale: string = 'en';

  @Output() viewChange: EventEmitter<string> = new EventEmitter();

  @Output() viewDateChange: EventEmitter<Date> = new EventEmitter();
}
