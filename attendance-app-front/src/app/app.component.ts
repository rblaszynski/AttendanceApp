import {Component, OnInit} from '@angular/core';
import {UiService} from "./services/ui/ui.service";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.less']
})
export class AppComponent implements OnInit {
  showMenu = false;
  darkModeActive: boolean;
  private currentTime: Date;
  intervalId;

  constructor(public ui: UiService) {

  }

  ngOnInit() {
    this.ui.darkModeState.subscribe((value => {
      this.darkModeActive = value;
    }));
    this.showDigitalClock();
  }

  toggleMenu() {
    this.showMenu = !this.showMenu;
  }

  modeToggleSwitch() {
    this.ui.darkModeState.next(!this.darkModeActive);
  }

  showDigitalClock() {
    this.currentTime = new Date();
    this.intervalId = setInterval(() => {
      this.showDigitalClock();
    }, 60000);

  }

  ngOnDestroy() {
    clearInterval(this.intervalId);
  }


}

