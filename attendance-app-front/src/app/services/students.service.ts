import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Student} from "../model/Student";
import {saveAs} from "file-saver";

@Injectable({
  providedIn: 'root'
})
export class StudentsService {

  private studentsUrl = 'http://localhost:5000/api/students/all';
  private filesUrl = 'http://localhost:5000/api/students/file';
  private studentUrl = 'http://localhost:5000/api/student';
  private getRecentCardUrl = 'http://localhost:5000/api/card/recent';

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
    this.http.get(this.filesUrl, {responseType: 'blob'}).subscribe(res => {
      let blob = new Blob([res], {type: "text/csv"});
      saveAs(blob, 'Students_list.csv');
    });
  }

  getLastCardID(): Observable<string> {
    return this.http.get<string>(this.getRecentCardUrl);
  }

}
