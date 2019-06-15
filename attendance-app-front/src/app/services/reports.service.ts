import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ReportsService {

  private reportUrl = 'http://localhost:5000/api/report';

  constructor(private http: HttpClient) {
  }

  generateReport(data): void {
    this.http.post(this.reportUrl, data)
      .subscribe((res) => console.log(res));
  }

}
