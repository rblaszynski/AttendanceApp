import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Student} from "../model/Student";

@Injectable({
  providedIn: 'root'
})
export class StudentsService {

  private studentsUrl = 'http://localhost:5000/api/students/all';

  constructor(private http: HttpClient) {
  }

  getStudents(): Observable<Student[]> {
    return this.http.get<Student[]>(this.studentsUrl);
  }

}
