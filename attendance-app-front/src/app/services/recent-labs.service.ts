import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Lecture} from "../model/Lecture";

@Injectable({
  providedIn: 'root'
})
export class RecentLabsService {

  private studentsUrl = 'http://localhost:5000/api/lecture/latest';

  constructor(private http: HttpClient) {
  }

  getRecentLabs(): Observable<Lecture> {
    return this.http.get<Lecture>(this.studentsUrl);
  }

}
