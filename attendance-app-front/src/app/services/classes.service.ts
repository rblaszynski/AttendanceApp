import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {CalendarEvent} from "calendar-utils";

@Injectable({
  providedIn: 'root'
})
export class ClassesService {

  private calendarUrl = 'http://localhost:5000/api/calendar/all';

  constructor(private http: HttpClient) {
  }

  getClasses(): Observable<CalendarEvent[]> {
    return this.http.get<CalendarEvent[]>(this.calendarUrl);
  }

}
