import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {saveAs} from 'file-saver';

@Injectable({
  providedIn: 'root'
})
export class ReportsService {

  private reportUrl = 'http://localhost:5000/api/report';

  constructor(private http: HttpClient) {
  }

  generateReport(data): void {
    this.http.post(this.reportUrl, data, {responseType: 'blob'})
      .subscribe(res => {
        let blob = new Blob([res], {type: 'text'});
        saveAs(blob, data.fileName);
      });
  }

}
