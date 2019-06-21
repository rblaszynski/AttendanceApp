import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Student} from "../model/Student";

@Injectable({
  providedIn: 'root'
})
export class StudentsService {

  private studentsUrl = 'http://localhost:5000/api/students/all';
  private filesUrl = 'http://localhost:5000/api/students/file';
  private studentUrl = 'http://localhost:5000/api/student';

  constructor(private http: HttpClient) {
  }

  getStudents(): Observable<Student[]> {
    return this.http.get<Student[]>(this.studentsUrl);
  }

  loadFile(file): void {
    this.http.post(this.filesUrl, file)
      .subscribe((res) => console.log(res));
  }

  addStudent(data): void {
    this.http.post(this.studentUrl, data)
      .subscribe((res) => console.log(res));
  }

  exportStudents(): void {
    this.http.get(this.filesUrl).subscribe();
  }

}
